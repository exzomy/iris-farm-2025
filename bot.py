import base64
import asyncio
from pyrogram import Client

# Публичные данные
API_ID = 1016382  # Замените на ваш API_ID
API_HASH = "c27834e5683d50a9bacf835a95ec4763"  # Замените на ваш API_HASH
CHAT_ID = -1002173353459  # Ваш чат

# Инициализация клиента с файлом сессии
app = Client(
    "ggww",
    api_id=API_ID,
    api_hash=API_HASH,
    workdir="."
)

async def send_messages():
    delay_minutes = 0
    while True:
        try:
            async with app:
                while True:
                    await app.send_message(
                        CHAT_ID,
                        f"⏰ Сообщение после {4*60 + delay_minutes} минут"
                    )
                    print(f"Сообщение отправлено (+{delay_minutes} минут)")
                    
                    await asyncio.sleep(4 * 3600 + delay_minutes * 60)
                    delay_minutes = (delay_minutes + 1) % 60
        except Exception as e:
            print(f"Ошибка: {e}. Повтор через 60 сек...")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print("🚀 Бот запущен с файлом сессии")
    asyncio.run(send_messages())
