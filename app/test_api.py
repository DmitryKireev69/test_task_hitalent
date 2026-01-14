from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch, MagicMock
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.main import app
from app.models import Chat, Massage
from app.database import get_db_async_db

mock_db_session = AsyncMock(spec=AsyncSession)


def test_create_chat_success():
    """Тест создания чата"""

    chat_data = {
        "title": "Тестовый чат",
    }

    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = 1
    mock_chat.title = "Тестовый чат"
    mock_chat.created_at = datetime.now()

    mock_db = AsyncMock()

    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock(side_effect=lambda obj: setattr(obj, 'id', 1))

    app.dependency_overrides[get_db_async_db] = lambda: mock_db

    with patch('app.routers.chats.Chat') as MockChat:
        MockChat.return_value = mock_chat

        with TestClient(app) as client:
            response = client.post("/chats/", json=chat_data)

    # Проверяем результат
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

    app.dependency_overrides.clear()

    assert response.status_code == 200

    response_data = response.json()
    assert "id" in response_data
    assert response_data["title"] == "Тестовый чат"


def test_create_message_in_chat_success():
    """Тест успешного создания сообщения в чате"""

    message_data = {
        "text": "Привет, это тестовое сообщение!",
        "chat_id": 1
    }

    mock_chat = MagicMock(spec=Chat)
    mock_chat.id = 1
    mock_chat.title = 'Тестовый чат'


    mock_message = MagicMock(spec=Massage)
    mock_message.id = 1
    mock_message.text = "Привет, это тестовое сообщение!"
    mock_message.chat_id = 1
    mock_message.created_at = datetime.now()

    mock_db = AsyncMock()

    mock_scalar_result = MagicMock()
    mock_scalar_result.one_or_none = MagicMock(return_value=mock_chat)
    mock_db.scalars = AsyncMock(return_value=mock_scalar_result)


    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()


    app.dependency_overrides[get_db_async_db] = lambda: mock_db


    with patch('app.routers.messeges.Massage') as MockMassage:
        MockMassage.return_value = mock_message

        with TestClient(app) as client:
            response = client.post("/chats/1/messages", json=message_data)

    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

    app.dependency_overrides.clear()

    assert response.status_code == 201

    response_data = response.json()
    assert "id" in response_data
    assert response_data["text"] == "Привет, это тестовое сообщение!"
    assert response_data["chat_id"] == 1
    assert "created_at" in response_data
