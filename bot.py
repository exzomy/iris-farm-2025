# bot.py
import asyncio
from pyrogram import Client

app = Client(
    "my_account",  # Используем созданный session-файл
    api_id=1016382,
    api_hash="c27834e5683d50a9bacf835a95ec4763",
    workdir="."
)

async def main():
    async with app:
        while True:
            try:
                await app.send_message(
                    -1002173353459,  # Ваш CHAT_ID
                    "⏰ Автоматическое сообщение"
                )
                print("Сообщение отправлено!")
                await asyncio.sleep(4 * 3600 + 60)  # 4ч 1мин
            except Exception as e:
                print(f"Ошибка: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
