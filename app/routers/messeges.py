from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas import CreateMassageSchema, MassageSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Massage, Chat
from app.database import get_db_async_db
from sqlalchemy import select

router = APIRouter(
    prefix="/chats",
    tags=["Сообщение"],)


@router.post('/{id}/messages', status_code=status.HTTP_201_CREATED, summary='Создать сообщение в чате',
             response_model=MassageSchema)
async def create_message_in_chat(data_massage: CreateMassageSchema, id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Создает сообщение"""
    result = await db.scalars(select(Chat).filter_by(id=id))
    chat = result.one_or_none()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Чат с идентификатором {id} не найден!')
    massage = Massage(**data_massage.model_dump())
    db.add(massage)
    await db.commit()
    return massage
