from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import String, func
from typing import List, Annotated

# Указал для дальнейшей масштабируемости можно вынести в отдельный файл common и использовать в других моделях
intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]

class Chat(Base):
    """Модель чата"""
    __tablename__ = 'chats'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(250))
    created_at: Mapped[created_at]
    massages: Mapped[List['Massage']] = relationship(
        back_populates='chat',
        cascade="all, delete-orphan"
    )
