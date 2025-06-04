import os
import base64
import asyncio
from pyrogram import Client

# Проверка и загрузка переменных окружения
def load_env():
    env_vars = {
        'API_ID': int(os.getenv("API_ID")),
        'API_HASH': os.getenv("API_HASH"),
        'TG_SESSION_BASE64': os.getenv("TG_SESSION_BASE64"),
        'CHAT_ID': int(os.getenv("CHAT_ID"))
    }
    
    if not all(env_vars.values()):
        missing = [k for k, v in env_vars.items() if not v]
        print(f"Ошибка: Отсутствуют переменные - {', '.join(missing)}")
        exit(1)
    
    return env_vars

# Восстановление сессии
def restore_session(session_b64):
    try:
        with open("my_account.session", "wb") as f:
            f.write(base64.b64decode(session_b64))
        print("Сессия успешно восстановлена")
    except Exception as e:
        print(f"Ошибка восстановления сессии: {e}")
        exit(1)

async def run_bot():
    env = load_env()
    restore_session(env['TG_SESSION_BASE64'])
    
    app = Client(
        "my_account",
        api_id=env['API_ID'],
        api_hash=env['API_HASH'],
        workdir=".",
        in_memory=True
    )

    delay_minutes = 0
    async with app:
        while True:
            try:
                await app.send_message(
                    env['CHAT_ID'],
                    f"⏰ Сообщение после {4*60 + delay_minutes} минут"
                )
                print(f"Сообщение отправлено (задержка +{delay_minutes} минут)")
                
                await asyncio.sleep(4 * 3600 + delay_minutes * 60)
                delay_minutes = (delay_minutes + 1) % 60
            except Exception as e:
                print(f"Ошибка: {e}. Повторная попытка через 60 секунд")
                await asyncio.sleep(60)

if __name__ == "__main__":
    print("🚀 Запуск Telegram бота")
    asyncio.run(run_bot())
