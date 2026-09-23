from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
)

from app.models.user import User
from app.routes.dependencies import get_current_user
from app.services.receipt_service import (
    validate_image,
    resize_image_if_needed,
    upload_receipt,
    extract_receipt_data
)

router = APIRouter(
    prefix="/receipts",
    tags=["Receipts"],
)
@router.post("")
@router.post("/", include_in_schema=False)
async def scan_receipt(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    content = await file.read()

    print("CONTENT TYPE:", file.content_type)
    print("FILE SIZE:", len(content))

    try:
        validate_image(content, file.content_type)

        content = resize_image_if_needed(content)

        receipt_data = extract_receipt_data(
            content,
            file.content_type,
        )
        uploaded_receipt = upload_receipt(content, file.filename)
        
        return {
            "receipt": receipt_data, 
            "receipt_url": uploaded_receipt["url"]
        }

    except ValueError as e:
        print("VALUE ERROR:", repr(e))

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        print("OTHER ERROR:", type(e))
        print("ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Could not scan receipt",
        )