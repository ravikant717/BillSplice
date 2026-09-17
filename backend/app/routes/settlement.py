from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.routes.dependencies import get_current_user
from app.models.user import User
from app.schemas.settlement import SettlementCreate, SettlementResponse
from app.services.settlement_service import create_settlement

router = APIRouter(
    prefix="/settlements",
    tags=["Settlements"],
)


@router.post(
    "",
    response_model=SettlementResponse,
)
def settle(
    settlement: SettlementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_settlement(
        settlement.group_id,
        current_user,
        settlement.to_user_id,
        settlement.amount,
        db,
    )