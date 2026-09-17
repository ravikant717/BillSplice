from PIL import Image
from fastapi import HTTPException
from app.db.database import settings
from app.schemas.receipt import ReceiptData
from google import genai
from google.genai import types
import io
import cloudinary
import cloudinary.uploader

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
}

MAX_FILE_SIZE_MB = 15
MAX_IMAGE_DIMENSION = 2048

api_key = (settings.GEMINI_API_KEY or "").strip()

client = genai.Client(api_key=api_key) if api_key else None

def validate_image(
    content: bytes,
    content_type: str,
) -> None:

    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError(
            "Only JPEG and PNG images are allowed"
        )

    size_mb = len(content) / (1024 * 1024)

    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(
            f"File must be smaller than {MAX_FILE_SIZE_MB} MB"
        )

    try:
        image = Image.open(
            io.BytesIO(content)
        )

        image.verify()

    except Exception:
        raise ValueError(
            "Invalid or corrupted image"
        )
def resize_image_if_needed(
    content: bytes,
) -> bytes:

    image = Image.open(
        io.BytesIO(content)
    )

    width, height = image.size

    if (
        width <= MAX_IMAGE_DIMENSION
        and height <= MAX_IMAGE_DIMENSION
    ):
        return content

    image.thumbnail(
        (
            MAX_IMAGE_DIMENSION,
            MAX_IMAGE_DIMENSION,
        ),
        Image.Resampling.LANCZOS,
    )

    output = io.BytesIO()

    # Keep the original format if possible
    image_format = image.format or "JPEG"

    if image_format == "JPEG":
        image.save(
            output,
            format="JPEG",
            quality=90,
            optimize=True,
        )
    else:
        image.save(
            output,
            format=image_format,
        )

    return output.getvalue()
def upload_receipt(
    content: bytes,
    filename: str,
) -> dict:

    result = cloudinary.uploader.upload(
        io.BytesIO(content),

        folder="billsplice/receipts",

        resource_type="image",
    )

    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }
    
def extract_receipt_data(
    content: bytes,
    content_type: str,
) -> ReceiptData:

    if not client:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured on the server",
        )

    prompt = """
Extract the information from this receipt.

Rules:
- Extract the merchant/store name if visible.
- Extract the receipt date if visible.
- Extract every purchased item and its price.
- Extract the final total amount.
- Do not invent missing information.
- Do not include subtotal, tax, discounts, tips, or service charges
  as purchased items.
- If information cannot be read confidently, omit it.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=content,
                mime_type=content_type,
            ),
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ReceiptData,
        ),
    )

    return ReceiptData.model_validate_json(
        response.text
    )