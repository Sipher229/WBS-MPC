from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.models.DocumentTracker import DocumentTracker
from app.schemas.OcrDocumentSchema import OcrDocumentSchema
from app.services.documentservice import DocumentService
from app.schemas.OrderOcrExtractSchema import OrderOcrExtractSchema

router = APIRouter()


@router.get("/processed/today", response_model=List[OcrDocumentSchema])
def read_processed_orders(
    service: DocumentService = Depends()
):
    orders: List[OcrDocumentSchema] = service.get_todays_processed_orders()
    if not orders:
        return []
    return orders


@router.get("/{doc_id}", response_model=OcrDocumentSchema)
def get_document_by_id(doc_id: str, doc_service: DocumentService = Depends()):
    document: DocumentTracker = doc_service.get_doc_by_id(doc_id)

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )
    return document
