from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List 
from app.schemas.join_group import JoinGroupRequest
from app.schemas.group_detail import GroupDetailResponse
from app.routes.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.balance import BalanceResponse
from app.schemas.settlement import SuggestedSettlementResponse
from app.services.expense_service import calculate_balances, simplify_balances

from app.schemas.group import GroupCreate, GroupResponse
from app.services.group_service import (
    create_group,
    get_groups,
    join_group,
    leave_group, 
    get_group_details
)
router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)


@router.post(
    "",
    response_model=GroupResponse,
)
def create_new_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return create_group(
        group.name,
        current_user,
        db,
    )


@router.get(
    "/{group_id}", 
    response_model=GroupDetailResponse   
)
def get_group_detail(
    group_id: UUID, 
    db: Session = Depends(get_db), 
):
    return get_group_details(group_id, db)

@router.get(
    "",
    response_model=List[GroupResponse],
)
def list_groups(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_groups(
        current_user,
        db,
    )
    
@router.post("/join")
def join(
    request: JoinGroupRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return join_group(
        request.invite_code,
        current_user,
        db,
    )
@router.delete("/{group_id}/leave")
def leave(
    group_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return leave_group(
        group_id,
        current_user,
        db,
    )
    
@router.get(
    "/{group_id}/balances",
    response_model=List[BalanceResponse],
)
def balances(
    group_id,
    db: Session = Depends(get_db),
):
    '''Fills up the balances table'''
    return calculate_balances(
        group_id,
        db,
    )

@router.get(
    "/{group_id}/settlements",
    response_model=list[SuggestedSettlementResponse],
)
def settlements(
    group_id,
    db: Session = Depends(get_db),
):
    return simplify_balances(
        group_id,
        db,
    )   