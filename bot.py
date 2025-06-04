import os
import base64
from pyrogram import Client

# Данные из Secrets GitHub
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_BASE64 = os.getenv("TG_SESSION_BASE64")

# Жёстко прописываем CHAT_ID (ваш чат -1002173353459)
CHAT_ID = -1002173353459

# Восстанавливаем сессию из base64
if SESSION_BASE64:
    with open("my_account.session", "wb") as f:
        f.write(base64.b64decode(SESSION_BASE64))

# Запускаем бота
app = Client("my_account", API_ID, API_HASH)

async def main():
    await app.send_message(CHAT_ID, "⏰ Прошло 4 часа! Сообщение от бота.") 

with app:
    app.loop.run_until_complete(main())
