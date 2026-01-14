from fastapi import FastAPI
from app.routers import chats, messeges
app = FastAPI(
    title='API чатов и сообщений'
)

app.include_router(chats.router)
app.include_router(messeges.router)

@app.get("/")
def root():
    """Корневой маршрут"""
    return {"message": "Добро пожаловать"}