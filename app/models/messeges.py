from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import ForeignKey, String, func
from typing import Annotated


# Указал для дальнейшей масштабируемости можно вынести в отдельный файл common и использовать в других моделях
intpk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]

class Massage(Base):
    """Модель сообщения"""
    __tablename__ = 'massages'

    id: Mapped[intpk]
    chat_id: Mapped[int] = mapped_column(ForeignKey('chats.id', ondelete='CASCADE'))
    text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[created_at]
    chat: Mapped['Chat'] = relationship(back_populates='massages')
