

import asyncio
from pyrogram import Client
from datetime import datetime

app = Client(
    "my_account",  # Используем созданный session-файл
    api_id=1016382,
    api_hash="c27834e5683d50a9bacf835a95ec4763",
    workdir="."
)

async def send_farming_message():
    async with app:
        while True:
            try:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = (
                    "фарма\n"
                    f"⏰ Сообщение отправлено в {current_time}"
                )
                
                await app.send_message(
                    -1001234567890,  # Замените на ваш CHAT_ID
                    message
                )
                print(f"✅ Сообщение отправлено в {current_time}")
                
                # Ждем ровно 4 часа 1 минуту (14 460 секунд)
                await asyncio.sleep(4 * 3600 + 60)
                
            except Exception as e:
                print(f"⚠️ Ошибка: {e}. Повтор через 5 минут...")
                await asyncio.sleep(300)

if __name__ == "__main
