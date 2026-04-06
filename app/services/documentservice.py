from typing import Optional, Dict, Any

from fastapi import Depends

from app.models.DocumentTracker import DocumentTracker
from app.models.PODataExtract import PODataExtract
from app.repositories.DocumentRepo import DocumentRepository
from app.utils.DocumentState import DocumentState


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
