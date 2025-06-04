import os
import base64
import asyncio
from pyrogram import Client

# Конфигурация
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH", "")
SESSION_BASE64 = os.getenv("TG_SESSION_BASE64", "")
CHAT_ID = int(os.getenv("CHAT_ID", 0))

# Проверка обязательных переменных
if not all([API_ID, API_HASH, SESSION_BASE64, CHAT_ID]):
    raise ValueError("Не все обязательные переменные окружения установлены")

# Восстановление сессии
session_file = "my_account.session"
try:
    with open(session_file, "wb") as f:
        f.write(base64.b64decode(SESSION_BASE64))
except Exception as e:
    raise ValueError(f"Ошибка восстановления сессии: {e}")

# Инициализация клиента с обработкой ошибок
app = Client(
    name="my_account",
    api_id=API_ID,
    api_hash=API_HASH,
    workdir=".",
    in_memory=True,  # Важно для GitHub Actions
    sleep_threshold=30  # Увеличиваем таймауты
)

async def send_messages():
    delay_minutes = 0
    while True:
        try:
            async with app:  # Автоматическое управление сессией
                while True:
                    await app.send_message(
                        chat_id=CHAT_ID,
                        text=f"⏰ Сообщение после {4*60 + delay_minutes} минут"
                    )
                    print(f"Сообщение отправлено (задержка: {delay_minutes} минут)")
                    
                    await asyncio.sleep(4 * 3600 + delay_minutes * 60)
                    delay_minutes = (delay_minutes + 1) % 60
        except Exception as e:
            print(f"Критическая ошибка: {e}")
            await asyncio.sleep(60)  # Пауза перед повторной попыткой

if __name__ == "__main__":
    print("🚀 Запуск бота с прогрессирующим интервалом")
    try:
        asyncio.run(send_messages())
    except KeyboardInterrupt:
        print("Бот остановлен")
    except Exception as e:
        print(f"Фатальная ошибка: {e}")
