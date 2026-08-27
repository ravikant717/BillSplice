from fastapi import HTTPException
from sqlmodel import Session, select, delete
from collections import defaultdict
from uuid import UUID
from decimal import Decimal, ROUND_HALF_UP
from app.models.group import Group
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.group_member import GroupMember
from app.models.user import User
from app.models.settlement import Settlement

TWO_PLACES = Decimal("0.01")

#Adding an expense
def create_expense(
    group_id: UUID,
    title: str,
    amount: Decimal,
    current_user: User,
    db: Session,
):
    #Get group 
    statement = select(Group).where(Group.id == group_id)
    group = db.exec(statement).first()
    
    if group is None:
        raise HTTPException(status_code=404, detail="Group not found")

    #Get all group members 
    statement = select(GroupMember).where(GroupMember.group_id == group_id)
    members = db.exec(statement).all()

    if len(members) == 0:
        raise HTTPException(
            status_code=400,
            detail="Group has no members",
        )

    #Check if current user belongs to the group
    if not any(member.user_id == current_user.id for member in members):
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group",
        )

    expense = Expense(
        group_id=group_id,
        paid_by=current_user.id,
        title=title,
        amount=amount,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    # Split evenly, rounded to cents. Any leftover cents from rounding
    # is assigned to the last split so all splits always sum to `amount`.
    n = len(members)
    
    base_split = (amount / n).quantize(TWO_PLACES, rounding=ROUND_HALF_UP)
    
    splits_total = base_split * n
    remainder = amount - splits_total  # multiple of 0.01, can be +/-

    for index, member in enumerate(members):
        split_amount = base_split
        if index == n - 1:
            split_amount += remainder  

        split = ExpenseSplit(
            expense_id=expense.id,
            user_id=member.user_id,
            amount=split_amount,
        )
        db.add(split)

    db.commit()

    return expense

#Gets the group expense history
def get_group_expenses(group_id, db: Session):
    statement = select(Expense).where(Expense.group_id == group_id).order_by(Expense.created_at.desc())
    return db.exec(statement).all()


def delete_expense(
    expense_id,
    db: Session,
    current_user: User,
):
    #Get the expense
    statement = select(Expense).where(Expense.id == expense_id)    
    expense = db.exec(statement).first()
    

    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")

    #Check if expense is deleted by the one who created it
    if expense.paid_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the person who created this expense can delete it.",
        )

    #Delete the expense
    statement = delete(ExpenseSplit).where(ExpenseSplit.expense_id == expense_id)
    db.exec(statement)
    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}


#balance map: {user: balance}
def get_balance_map(
    group_id,
    db: Session,
):
    
    balances = defaultdict(Decimal)
    #get the expenses in the group 
    expenses = db.exec(select(Expense).where(Expense.group_id == group_id)).all()



    #Get all splits belonging to those expenses 
    splits = db.exec(
        select(ExpenseSplit)
        .join(Expense, ExpenseSplit.expense_id == Expense.id)
        .where(Expense.group_id == group_id)
    ).all()
    
    #Add what each person paid
    for expense in expenses:
        balances[str(expense.paid_by)] += Decimal(expense.amount)

    #Subtract what each person owes
    for split in splits: 
        balances[str(split.user_id)] -= Decimal(split.amount)
        
    settlements = db.exec(
        select(Settlement).where(
            Settlement.group_id == group_id
        )
    ).all()
    
    for settlement in settlements: 
        balances[str(settlement.from_user_id)] += Decimal(settlement.amount)
        
        balances[str(settlement.to_user_id)] -= Decimal(settlement.amount)

    #if balance(a) > balance(b) it means that a will get more money than b, or a will pay less money than b
    return balances


def calculate_balances(
    group_id,
    db: Session,
):
    balances = get_balance_map(group_id, db)
    user_ids = list(balances.keys())
    
    users = db.exec(select(User).where(User.id.in_(user_ids))).all()
    
    user_map = {
        str(user.id): user 
        for user in users
    }
    
    result = []

    for user_id, balance in balances.items():
        user = user_map.get(str(user_id))

        if user is None:
            continue  # user no longer exists; skip rather than crash

        result.append(
            {
                "user": user.name,
                "user_id": user.id,
                "balance": balance.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
            }
        )

    return result


def simplify_balance_map(group_id, db: Session):
    balances = get_balance_map(group_id, db)


    #Seperate creditors and debitors 
    debtors = []
    creditors = []

    for user_id, balance in balances.items():
        balance = balance.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)

        if balance < 0:
            debtors.append({"user_id": user_id, "amount": -balance})
        elif balance > 0:
            creditors.append({"user_id": user_id, "amount": balance})

    i = 0
    j = 0

    settlements = []

    '''
        i -> j (settlement)
        if i has less amount, means i only owes less amount so settle that only 
        if j has less amount, means j got that much money to get so dont send extra
    '''
    
    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i]["amount"], creditors[j]["amount"])

        settlements.append(
            {
                "from_user_id": debtors[i]["user_id"],
                "to_user_id": creditors[j]["user_id"],
                "amount": amount.quantize(TWO_PLACES, rounding=ROUND_HALF_UP),
            }
        )

        debtors[i]["amount"] -= amount
        creditors[j]["amount"] -= amount

        if debtors[i]["amount"] <= 0: #ith debt finished
            i += 1

        if creditors[j]["amount"] <= 0: #jth received all the money
            j += 1

    return settlements


def simplify_balances(group_id, db: Session):
    settlements = simplify_balance_map(group_id, db)

    if not settlements: 
        return []


    user_ids = set()
    

    for settlement in settlements:
        user_ids.add(settlement["from_user_id"])
        user_ids.add(settlement["to_user_id"])
        
    statement = select(User).where(User.id.in_(user_ids))
    users = db.exec(statement).all()
    
    user_map = {
        str(user.id): user 
        for user in users
    }
    
    result = []
    
    for settlement in settlements: 
        from_user = user_map.get(str(settlement["from_user_id"]))
        to_user = user_map.get(str(settlement["to_user_id"]))

        if from_user is None or to_user is None: 
            continue 
        
        result.append({
            "from_user": from_user.name, 
            "from_user_id": from_user.id, 
            "to_user": to_user.name, 
            "to_user_id": to_user.id, 
            "amount": settlement["amount"]            
        })
        
    return result

def get_overall_balance(
    current_user: User,
    db: Session,
):
    memberships = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id)
        .all()
    )

    total = Decimal("0")

    for membership in memberships:
        balances = get_balance_map(membership.group_id, db)
        total += balances.get(str(current_user.id), Decimal("0"))

    return {"balance": total.quantize(TWO_PLACES, rounding=ROUND_HALF_UP)}