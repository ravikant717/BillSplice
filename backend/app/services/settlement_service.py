from app.models.settlement import Settlement
from app.models.group_member import GroupMember

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.services.expense_service import get_balance_map

def create_settlement(
    group_id,
    current_user,
    to_user_id,
    amount,
    db: Session,
):
    # Verify payer is in the group
    payer = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == current_user.id,
        )
        .first()
    )

    if payer is None:
        raise HTTPException(
            status_code=403,
            detail="You are not a member of this group",
        )

    # Verify receiver is in the group
    receiver = (
        db.query(GroupMember)
        .filter(
            GroupMember.group_id == group_id,
            GroupMember.user_id == to_user_id,
        )
        .first()
    )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver is not a member of this group",
        )

    balances = get_balance_map(
    group_id,
    db,
    )

    payer_balance = balances[str(current_user.id)]

    if payer_balance >= 0:
        raise HTTPException(
            status_code=400,
            detail="You don't owe anyone anything.",
        )

    if amount > abs(payer_balance):
        raise HTTPException(
            status_code=400,
            detail="Settlement amount exceeds your debt.",
        )
    settlement = Settlement(
        group_id=group_id,
        from_user_id=current_user.id,
        to_user_id=to_user_id,
        amount=amount,
    )

    db.add(settlement)
    db.commit()
    db.refresh(settlement)

    return settlement