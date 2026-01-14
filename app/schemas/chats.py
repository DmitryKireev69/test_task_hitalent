from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, List
from datetime import datetime

class CreateChatSchema(BaseModel):
    title: Annotated[str, Field(max_length=200, description="Название чата")]

    model_config = ConfigDict(
        from_attributes=True,
        extra='forbid'
    )

class ChatSchema(CreateChatSchema):
    id: Annotated[int, Field(description='Идентификатор чата')]
    created_at: Annotated[datetime, Field(description='Дата создания чата')]

class ChatRelSchema(ChatSchema):
    massages: List['MassageSchema']