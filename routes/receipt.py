from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ReceiptRequest(BaseModel):
    data: str

@router.post("/")
def create_receipt(receipt: ReceiptRequest):
    return {
        "message": "Receipt created successfully",
        "data": receipt.data
    }
