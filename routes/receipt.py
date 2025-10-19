from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import base64
import requests
import json
import os
from utils.standardize import smart_standardize


router = APIRouter()


class Item(BaseModel):
    name: str
    price: float
    quantity: int
    unit: str  # Added field for kgs, pieces, lbs, etc.


class ReceiptResponse(BaseModel):
    items: List[Item]
    total: float


@router.post("/", response_model=ReceiptResponse)
async def process_receipt(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        mime_type = file.content_type or "image/png"
        base64_image = base64.b64encode(contents).decode("utf-8")
        data_uri = f"data:{mime_type};base64,{base64_image}"

        api_key = os.getenv("PERPLEXITY_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Perplexity API key not configured")

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Updated schema includes 'unit'
        payload = {
            "model": "sonar-pro",
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "items": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "price": {"type": "number"},
                                        "quantity": {"type": "number"},
                                        "unit": {"type": "string"}
                                    },
                                    "required": ["name", "price", "quantity", "unit"]
                                }
                            },
                            "total": {"type": "number"}
                        },
                        "required": ["items", "total"]
                    }
                }
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Extract all items, their quantities, units (like kg, lbs, pieces, or count), "
                                "and total from this receipt image. "
                                "Return a JSON exactly matching the provided schema."
                            ),
                        },
                        {"type": "image_url", "image_url": {"url": data_uri}},
                    ],
                }
            ],
        }

        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            headers=headers,
            json=payload,
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"]

        # Parse AI response
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            try:
                result = json.loads(content.replace("'", '"'))
            except Exception:
                raise HTTPException(status_code=500, detail="Failed to parse AI response")

        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        # Use your custom normalization function
        result["items"] = smart_standardize(result["items"])

        return ReceiptResponse(**result)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
