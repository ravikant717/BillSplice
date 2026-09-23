from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import List
from uuid import UUID

from app.db.database import get_db
from app.models.user import User
from app.routes.dependencies import get_current_user
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.schemas.balance import OverallBalanceResponse
from app.schemas.pagination import PaginatedResponse
from app.services.expense_service import create_expense, get_overall_balance, get_group_expenses, delete_expense

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "",
    response_model=ExpenseResponse,
)
@router.post(
    "/",
    response_model=ExpenseResponse,
    include_in_schema=False,
)
def add_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    '''
        Add expenses
    '''
    return create_expense(
        expense.group_id,
        expense.title,
        expense.amount,
        expense.receipt_url, 
        current_user,
        db,
    )
    
@router.get(
    "/groups/{group_id}",
    response_model=PaginatedResponse[ExpenseResponse],
)
def history(
    group_id: UUID,
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
):
    '''Get the list of all expenses'''
    return get_group_expenses(
        group_id,
        db,
        page,
        page_size,
    )
    
@router.delete("/{expense_id}")
def remove_expense(
    expense_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    '''Delete an expense'''
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