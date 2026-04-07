from datetime import date

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, update, func, or_
from typing import Optional, Dict, Any, List

from app.database import get_db
from app.models.PODataExtract import PODataExtract, PODataExtractItem
from app.models.DocumentTracker import DocumentTracker
from app.utils.DocumentState import DocumentState


class DocumentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_doc_by_id(self, document_id: str) -> Optional[DocumentTracker]:
        statement = select(DocumentTracker).where(DocumentTracker.document_id == document_id)
        return self.db.execute(statement).scalar_one_or_none()

    def update_document_with_extraction(self, doc: DocumentTracker, payload: Dict[str, Any]) -> DocumentTracker:
        try:
            doc.status = DocumentState.PROCESSED

            # Initialize the extraction record
            purchase_order = PODataExtract(
                delivery_address=payload.get("delivery_address"),
                order_date=payload.get("order_date"),
                buyer_phone=payload.get("buyer_phone"),
                delivery_date=payload.get("delivery_date"),
                grand_total=payload.get("grand_total"),
                customer_name=payload.get("customer_name"),
                supplier_name=payload.get("supplier_name"),
                buyer_email=payload.get("buyer_email"),
                purchase_order_number=payload.get("purchase_order_number")
            )

            # Map line items if they exist
            line_items = payload.get("line_items", [])
            for item in line_items:
                new_item = PODataExtractItem(
                    product_supplier_code=item.get("product_supplier_code"),
                    product_description=item.get("product_description"),
                    quantity_ordered=item.get("quantity_ordered"),
                    cost=item.get("cost")
                )
                purchase_order.items.append(new_item)

            doc.extracted_data = purchase_order
            self.db.commit()
            self.db.refresh(doc)
            return doc

        except Exception as e:
            self.db.rollback()
            raise e

    def create_document(
            self,
            document_id: str,
            filename: str,
            status: DocumentState = DocumentState.PENDING,
            extracted_data: Optional[PODataExtract] = None
    ) -> DocumentTracker:
        """
        Creates a new entry in the DocumentTracker table.
        Defaults to 'UPLOADED' status unless specified otherwise.
        """
        try:
            new_doc = DocumentTracker(
                document_id=document_id,
                filename=filename,
                status=status,
                extracted_data=extracted_data
            )

            self.db.add(new_doc)
            self.db.commit()
            self.db.refresh(new_doc)
            return new_doc

        except Exception as e:
            self.db.rollback()
            # Log error here with a logger.
            raise e

    def update_doc_state(self, doc_id: str, new_state: DocumentState):
        stmt = (
            update(DocumentTracker)
            .where(DocumentTracker.document_id == doc_id)
            .values(status=new_state)
            .returning(DocumentTracker)
        )
        result = self.db.execute(stmt)
        self.db.commit()
        return result.scalar_one()

    def get_processed_orders_by_date(self, target_date: date) -> List[DocumentTracker]:
        # Filters by status and casts the 'created_at' timestamp to a date for comparison
        query = select(DocumentTracker).where(
                or_(
                    DocumentTracker.status == DocumentState.PROCESSED,
                    DocumentTracker.status == DocumentState.NORMALIZED,
                ))
        # .where(func.date(DocumentTracker.updated_at) == target_date)

        result = self.db.execute(query)
        return list(result.scalars().all())
