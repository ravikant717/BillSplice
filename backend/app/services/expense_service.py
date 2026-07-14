from fastapi import HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.models.group import Group
from app.models.expense import Expense
from app.models.expense_split import ExpenseSplit
from app.models.group_member import GroupMember
from app.models.user import User
from app.models.group_member import GroupMember
from app.models.group import Group
from app.models.settlement import Settlement
def create_expense(
    group_id,
    title,
    amount,
    current_user: User,
    db: Session,
):

    members = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    if len(members) == 0:
        raise HTTPException(
            status_code=400,
            detail="Group has no members",
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

    split_amount = amount / len(members)

    for member in members:

        split = ExpenseSplit(
            expense_id=expense.id,
            user_id=member.user_id,
            amount=split_amount,
        )

        db.add(split)

    db.commit()

    return expense


def get_balance_map(
    group_id,
    db: Session,
):
    balances = defaultdict(float)

    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    for expense in expenses:

        balances[str(expense.paid_by)] += float(expense.amount)

        splits = (
            db.query(ExpenseSplit)
            .filter(
                ExpenseSplit.expense_id == expense.id
            )
            .all()
        )

        for split in splits:
            balances[str(split.user_id)] -= float(split.amount)

    settlements = (
    db.query(Settlement)
    .filter(Settlement.group_id == group_id)
    .all()
)

    for settlement in settlements:

        # The debtor paid money, so their debt decreases
        balances[str(settlement.from_user_id)] += float(settlement.amount)

        # The creditor received money, so their credit decreases
        balances[str(settlement.to_user_id)] -= float(settlement.amount)
    return balances

def calculate_balances(
    group_id,
    db: Session,
):
    balances = get_balance_map(
        group_id,
        db,
    )

    result = []

    for user_id, balance in balances.items():

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        result.append(
            {
                "user": user.name,
                "balance": round(balance, 2),
            }
        )

    return result
def simplify_balance_map(group_id, db: Session):

    balances = get_balance_map(group_id, db)

    debtors = []
    creditors = []

    for user_id, balance in balances.items():

        if balance < 0:

            debtors.append(
                {
                    "user_id": user_id,
                    "amount": -balance,
                }
            )

        elif balance > 0:

            creditors.append(
                {
                    "user_id": user_id,
                    "amount": balance,
                }
            )

    i = 0
    j = 0

    settlements = []

    while i < len(debtors) and j < len(creditors):

        amount = min(
            debtors[i]["amount"],
            creditors[j]["amount"],
        )

        settlements.append(
            {
                "from_user_id": debtors[i]["user_id"],
                "to_user_id": creditors[j]["user_id"],
                "amount": round(amount, 2),
            }
        )

        debtors[i]["amount"] -= amount
        creditors[j]["amount"] -= amount

        if debtors[i]["amount"] == 0:
            i += 1

        if creditors[j]["amount"] == 0:
            j += 1

    return settlements
def simplify_balances(group_id, db: Session):

    settlements = simplify_balance_map(
        group_id,
        db,
    )

    result = []

    for settlement in settlements:

        from_user = (
            db.query(User)
            .filter(User.id == settlement["from_user_id"])
            .first()
        )

        to_user = (
            db.query(User)
            .filter(User.id == settlement["to_user_id"])
            .first()
        )

        result.append(
            {
                "from_user": from_user.name,
                "from_user_id": from_user.id,

                "to_user": to_user.name,
                "to_user_id": to_user.id,

                "amount": settlement["amount"],
            }
        )

    return result
def get_group_expenses(group_id, db: Session):

    expenses = (
        db.query(Expense)
        .filter(Expense.group_id == group_id)
        .all()
    )

    return expenses

def delete_expense(
    expense_id,
    db: Session,
    current_user: User
):

    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id)
        .first()
    )

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found",
        )
    if expense.paid_by != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Only the person who created this expense can delete it.",
        )
    db.query(ExpenseSplit).filter(
        ExpenseSplit.expense_id == expense_id
    ).delete()

    db.delete(expense)

    db.commit()

    return {
        "message": "Expense deleted"
    }
    
def get_overall_balance(
    current_user: User,
    db: Session,
):
    memberships = (
        db.query(GroupMember)
        .filter(GroupMember.user_id == current_user.id)
        .all()
    )

    total = 0

    for membership in memberships:
        balances = calculate_balances(
            membership.group_id,
            db,
        )

        for balance in balances:
            if balance["user"] == current_user.name:
                total += balance["balance"]

    return {
        "balance": total,
    }    