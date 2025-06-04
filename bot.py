import os
import base64
import asyncio
from pyrogram import Client

# Конфигурация
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_BASE64 = os.getenv("TG_SESSION_BASE64")
CHAT_ID = int(os.getenv("CHAT_ID"))

# Восстановление сессии
if SESSION_BASE64:
    with open("my_account.session", "wb") as f:
        f.write(base64.b64decode(SESSION_BASE64))

# Инициализация клиента
app = Client(
    "my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    workdir="."  # Ищем session-файл в текущей директории
)

async def main():
    delay_minutes = 0
    while True:
        try:
            await app.send_message(CHAT_ID, f"⏰ Сообщение после {4*60 + delay_minutes} минут")
            print(f"Сообщение отправлено в {delay_minutes} минут")
            
            await asyncio.sleep(4 * 3600 + delay_minutes * 60)
            delay_minutes = (delay_minutes + 1) % 60  # Сброс через час
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    print("Запуск бота...")
    app.run(main())
