from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from uuid import UUID
from app.api.dependencies import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.schemas.balance import BalanceResponse, OverallBalanceResponse
from app.schemas.settlement import SettlementResponse, SuggestedSettlementResponse
from app.services.expense_service import create_expense, get_overall_balance, calculate_balances, simplify_balances, get_group_expenses, delete_expense
router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "",
    response_model=ExpenseResponse,
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return create_expense(
        expense.group_id,
        expense.title,
        expense.amount,
        current_user,
        db,
    )
    
@router.get(
    "/groups/{group_id}/balances",
    response_model=List[BalanceResponse],
)
def balances(
    group_id,
    db: Session = Depends(get_db),
):

    return calculate_balances(
        group_id,
        db,
    )
    
@router.get(
    "/groups/{group_id}/settlements",
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
    
@router.get(
    "/groups/{group_id}",
    response_model=list[ExpenseResponse],
)
def history(
    group_id: UUID,
    db: Session = Depends(get_db),
):

    return get_group_expenses(
        group_id,
        db,
    )
    
@router.delete("/{expense_id}")
def remove_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return delete_expense(
        expense_id,
        db,
        current_user
    )
    
@router.get(
    "/overall-balance",
    response_model=OverallBalanceResponse,
)
def overall_balance(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_overall_balance(
        current_user,
        db,
    )