from typing import List, Optional, Dict
import re
from fastapi import Depends, HTTPException
from rapidfuzz import process, fuzz
from app.models.ProductCatalog import ProductCatalog
from app.repositories.ProductRepository import ProductRepository
from app.repositories.DocumentRepo import DocumentRepository
from app.schemas.sage300Oorderreview import OrderHeaderReview, OrderDetailReview
from app.utils.DocumentState import DocumentState


class NormaliserService:
    # Regex: letter - 2digits - 3digits - 3letters - 4digits (optional hyphens)
    PROD_CODE_PATTERN = re.compile(
        r"^[A-Z]-?\d+-?\d+-?[A-Z]+-?[A-Z]*-?\d+$",
        re.IGNORECASE
    )
    REVIEW_REASON_PROD_NOT_FOUND = "No matching product found in existing catalog"
    REVIEW_REASON_DESC_NOT_CLOSE = "Description is not close enough"
    NEEDS_REVIEW_THRESHOLD = 70

    def __init__(self, prod_repo: ProductRepository = Depends(), doc_repo: DocumentRepository = Depends()):
        self.prod_repo = prod_repo
        self.doc_repo = doc_repo

    def _fuzzy_match(self, target_desc: str, products: List[ProductCatalog]) -> Optional[OrderDetailReview]:
        detail_for_review: Optional[OrderDetailReview] = None
        # Map descriptions to the actual objects
        if not products:
            return None
        choices_map: Dict[str, ProductCatalog] = {}
        for p in products:
            # Ensure description is a string and not None
            desc_value = str(p.product) if p.product else ""
            if desc_value:
                choices_map[desc_value] = p
        if not choices_map:
            return None

        # Explicitly define the list of strings
        # This satisfies the (str, Iterable[str], Scorer) signature

        choices_list: List[str] = list(choices_map.keys())
        # Find the best match
        best_match = process.extractOne(target_desc, choices_list, scorer=fuzz.WRatio)  # type: ignore

        if best_match:  # 70 is a standard confidence threshold
            strong_match_desc, score, _ = best_match
            match_product = choices_map[strong_match_desc]
            detail_for_review = OrderDetailReview(
                item=match_product.item,
                qty_ordered=match_product.qty_ord,
                unit_price=match_product.price,
                original_description=target_desc,
                suggested_item_code=match_product.item,
                match_score=round(score, 2),
                needs_review=round(score, 2) < self.NEEDS_REVIEW_THRESHOLD,
                review_reason=self.REVIEW_REASON_DESC_NOT_CLOSE
            )
            return detail_for_review
        return detail_for_review

    # def _fuzzy_match_address(self, target_address: str, product: ProductCatalog) -> Optional[str]:
    #     if product is None:
    #         return None
    #     suspected_address = product.ship_to_address_1

    def normalize_doc(self, doc_id: str) -> OrderHeaderReview:
        doc = self.doc_repo.get_doc_by_id(doc_id)
        # Extract variables from doc
        if doc:
            customer_name = doc.extracted_data.customer_name
            address = doc.extracted_data.delivery_address

        else:
            raise HTTPException(status_code=404, detail="no such document")

        if not customer_name and not address:
            print("verify customer exists")
            raise HTTPException(
                status_code=422,
                detail="Order cannot be normalized."
            )

        if (doc.status == DocumentState.PROCESSED or doc.status == DocumentState.NORMALIZED) and doc.extracted_data:
            order_for_review: OrderHeaderReview = OrderHeaderReview(
                customer_number="number",
                order_date=doc.extracted_data.order_date,
                order_details=[],
                expected_ship_date=doc.extracted_data.delivery_date,
                purchase_order_number=doc.extracted_data.purchase_order_number
            )
            if doc.extracted_data.delivery_address:
                address_components: ProductCatalog = self.prod_repo.get_ship_to_address(
                    doc.extracted_data.delivery_address,
                    doc.extracted_data.customer_name
                )
                order_for_review.ship_to_address_line_1 = address_components.ship_to_address_1
                order_for_review.ship_to_name = address_components.ship_to_name
                order_for_review.ship_to_city = address_components.ship_to_city
                order_for_review.ship_to_address_line_2 = address_components.ship_to_address_2

            try:

                line_items = doc.extracted_data.items
                if line_items:
                    for item in line_items:  # iterate over each item and normalize it
                        product_code = item.product_supplier_code
                        description = item.product_description
                        price = item.cost
                        detail_for_review: Optional[OrderDetailReview] = None
                        if product_code and bool(self.PROD_CODE_PATTERN.fullmatch(product_code)):  # make sure the \
                            # provided code matches our pattern
                            results = self.prod_repo.get_products_by_product_code(
                                customer_name, 
                                address, 
                                product_code
                            )  # should first isolate all products by customer.
                            detail_for_review = self._fuzzy_match(description, results)
                            if detail_for_review:
                                if not detail_for_review.needs_review:
                                    order_for_review.is_fully_normalized = True

                                if detail_for_review.needs_review:
                                    order_for_review.total_items_needing_review += 1

                                order_for_review.order_details.append(detail_for_review)  # add this \
                                # order detail to the order details of the order header
                        elif price is not None:   # use price to match if the price is given
                            results = self.prod_repo.get_products_by_customer_and_price(customer_name, address, price)
                            detail_for_review = self._fuzzy_match(description, results)
                            if detail_for_review:
                                if not detail_for_review.needs_review:
                                    order_for_review.is_fully_normalized = True
                                if detail_for_review.needs_review:
                                    order_for_review.total_items_needing_review += 1

                                order_for_review.order_details.append(detail_for_review)  # add this order\
                                # detail to the order details of the order header
                        elif price is None and description.strip() and (customer_name.strip() or address.strip()):
                            # use description if the price is not available
                            results = self.prod_repo.get_products_by_description(customer_name, address, description)
                            detail_for_review = self._fuzzy_match(description, results)
                            if detail_for_review:
                                if not detail_for_review.needs_review:
                                    order_for_review.is_fully_normalized = True
                                if detail_for_review.needs_review:
                                    order_for_review.total_items_needing_review += 1

                                order_for_review.order_details.append(detail_for_review)  # add this order detail\
                                # to the order details of the order header
                        if not detail_for_review:   # if none of the above conditions apply, append the original data.
                            detail_for_review = OrderDetailReview(
                                item=product_code,
                                unit_price=price,
                                qty_ordered=item.quantity_ordered,
                                original_description=description,
                                suggested_item_code=product_code,
                                needs_review=True,
                                review_reason=self.REVIEW_REASON_PROD_NOT_FOUND
                            )

                            order_for_review.order_details.append(detail_for_review)  # add this order detail to the \
                            # order details of the order header
                    self.doc_repo.update_doc_state(doc.document_id, DocumentState.NORMALIZED)
                return order_for_review
            except Exception as e:
                print(f"Error normalizing doc: {e}")
                raise HTTPException(status_code=404, detail="Not Found")

        else:
            raise HTTPException(status_code=422, detail="cannot process document")

