from pydantic import BaseModel, ConfigDict


class NormaliseRequest(BaseModel):
    document_id: str

    model_config = ConfigDict(from_attributes=True)
