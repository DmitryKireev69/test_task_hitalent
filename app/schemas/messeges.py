from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from datetime import datetime

class CreateMassageSchema(BaseModel):
    text: Annotated[str, Field(max_length=5000, description='Сообщение')]
    chat_id: Annotated[int, Field(description='Идентификатор чата')]

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )

class MassageSchema(CreateMassageSchema):
    id: Annotated[int, Field(description='Идентификатор сообщения')]
    created_at: Annotated[datetime, Field(description='Дата создания сообщения')]

class MassageRelSchema(MassageSchema):
    chat: 'ChatSchema'