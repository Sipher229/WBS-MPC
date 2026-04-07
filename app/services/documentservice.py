from datetime import date
from typing import Optional, Dict, Any, List

from fastapi import Depends, HTTPException

from app.models.DocumentTracker import DocumentTracker
from app.models.PODataExtract import PODataExtract
from app.repositories.DocumentRepo import DocumentRepository
from app.schemas.OcrDocumentSchema import OcrDocumentSchema
from app.utils.DocumentState import DocumentState
from app.schemas.OrderOcrExtractSchema import OrderOcrExtractSchema


class DocumentService:
    def __init__(self, doc_repo: DocumentRepository = Depends()):
        self.doc_repo = doc_repo

    def get_doc_by_id(self, document_id: str) -> Optional[DocumentTracker]:
        return self.doc_repo.get_doc_by_id(document_id)

    def update_document_with_extraction(self, doc: DocumentTracker, payload: Dict[str, Any]) -> DocumentTracker:
        return self.doc_repo.update_document_with_extraction(doc, payload)

    def create_document(
            self,
            document_id: str,
            filename: str,
            status: DocumentState = DocumentState.PENDING,
            extracted_data: Optional[PODataExtract] = None
    ) -> DocumentTracker:
        return self.doc_repo.create_document(document_id, filename, status, extracted_data)

    def get_todays_processed_orders(self) -> List[OcrDocumentSchema]:

        try:

            today = date.today()
            orders = self.doc_repo.get_processed_orders_by_date(today)

            # FastAPI/Pydantic v2 will handle the conversion via 'from_attributes=True'
            return [OcrDocumentSchema.model_validate(order) for order in orders]
        except Exception as e:
            print(f"ERROR: Unable to get docs {e}")
            raise HTTPException(status_code=500, detail="unable to get documents")
