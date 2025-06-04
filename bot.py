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
    while True:
        try:
            async with app:
                # Отправка сообщения
                await app.send_message(
                    -1001234567890,  # Замените на ваш CHAT_ID
                    f"фарма\n
                    ⏰ Сообщение отправлено в {datetime.now().strftime('%H:%M:%S')}"
                )
                print(f"✅ Сообщение отправлено! Следующее через 4ч 1мин")

                # Точная задержка 4ч 1мин (14 460 секунд)
                await asyncio.sleep(4 * 3600 + 60)

        except Exception as e:
            print(f"⚠️ Ошибка: {e}. Повтор через 5 минут...")
            await asyncio.sleep(300)  # Ждем 5 минут при ошибке

if __name__ == "__main__":
    print("🚀 Бот запущен (интервал: 4ч 1мин)")
    asyncio.run(main())
