from pydantic import BaseModel, ConfigDict
from app.schemas.OrderOcrExtractSchema import OrderOcrExtractSchema


class OcrDocumentSchema(BaseModel):
    status: str
    filename: str
    extracted_data: OrderOcrExtractSchema | None
    document_id: str

    model_config = ConfigDict(from_attributes=True)
