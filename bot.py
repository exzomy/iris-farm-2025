import os
import base64
from pyrogram import Client

# Получаем данные из Secrets
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_BASE64 = os.getenv("TG_SESSION_BASE64")
CHAT_ID = int(os.getenv("CHAT_ID"))  # Опционально, если бот пишет в чат

# Восстанавливаем сессию
if SESSION_BASE64:
    with open("my_account.session", "wb") as f:
        f.write(base64.b64decode(SESSION_BASE64))

# Запускаем клиента
app = Client("my_account", API_ID, API_HASH)

async def main():
    await app.send_message(CHAT_ID, "Сообщение от бота!") 

with app:
    app.loop.run_until_complete(main())
