from pydantic import BaseModel, ConfigDict


class MyBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

