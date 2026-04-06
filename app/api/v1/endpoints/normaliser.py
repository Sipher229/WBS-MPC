from typing import List

from fastapi import APIRouter, Depends

from app.schemas.NormaliseRequest import NormaliseRequest
from app.schemas.ProductCatalogSchema import ProductCatalogSchema
from app.schemas.sage300Oorderreview import OrderHeaderReview
from app.services.normaliser_service import NormaliserService

router = APIRouter()


@router.post("/process", response_model=OrderHeaderReview)
def normalize_doc(
        request_data: NormaliseRequest,
        normalizer_service: NormaliserService = Depends(),
):
    data: OrderHeaderReview = normalizer_service.normalize_doc(request_data.document_id)
    return data
