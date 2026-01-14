from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import selectinload, aliased
from app.models import Chat, Massage
from app.schemas import CreateChatSchema, ChatSchema, ChatRelSchema
from app.database import get_db_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter(
    prefix="/chats",
    tags=["Чат"],
)

async def get_chat(chat_id: int, db: AsyncSession) -> Chat:
    """Получить чат"""
    result = await db.scalars(select(Chat).filter_by(id=chat_id))
    chat = result.one_or_none()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Чат с идентификатором {chat_id} не найден!')
    return chat

@router.post('/', response_model=ChatSchema, summary='Создать чат')
async def create_chat(data_chat: CreateChatSchema, db: AsyncSession = Depends(get_db_async_db)):
    """Создает чат"""
    chat = Chat(**data_chat.model_dump())
    db.add(chat)
    await db.commit()
    return chat


@router.delete('/{id}', summary='Удалить чат', status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: int, db: AsyncSession = Depends(get_db_async_db)):
    """Удаляет чат"""
    chat = await get_chat(id, db)
    await db.delete(chat)
    await db.commit()
    return None


@router.get('/{id}', summary='Получить чат с сообщениями по идентификатору' )
async def get_chat_by_id(
        id: int,
        db:AsyncSession = Depends(get_db_async_db),
        limit: int = Query(20, ge=20, le=100)
):
    """Получение чата с сообщениями по идентификатору"""

    subquery = (
        select(Massage.id)
        .filter_by(chat_id=id)
        .order_by('created_at')
        .limit(limit)
    )

    query = (
        select(Chat)
        .options(
            selectinload(
                Chat.massages.and_(
                    Massage.id.in_(select(subquery.c.id))
                )
            )
        )
        .filter_by(id=id)
    )

    res = await db.scalars(query)
    result_orm = res.all()
    result_dto = [ChatRelSchema.model_validate(row, from_attributes=True) for row in result_orm]
    return result_dto
