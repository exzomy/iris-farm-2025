import os
import base64
import asyncio
from pyrogram import Client

# Улучшенная проверка переменных окружения
def check_env_vars():
    required_vars = {
        'API_ID': os.getenv("API_ID"),
        'API_HASH': os.getenv("API_HASH"),
        'TG_SESSION_BASE64': os.getenv("TG_SESSION_BASE64"),
        'CHAT_ID': os.getenv("CHAT_ID")
    }
    
    missing_vars = [name for name, value in required_vars.items() if not value]
    if missing_vars:
        print(f"❌ Отсутствуют переменные окружения: {', '.join(missing_vars)}")
        print("Пожалуйста, добавьте их в Secrets GitHub!")
        exit(1)
    
    try:
        return {
            'api_id': int(required_vars['API_ID']),
            'api_hash': required_vars['API_HASH'],
            'session_b64': required_vars['TG_SESSION_BASE64'],
            'chat_id': int(required_vars['CHAT_ID'])
        }
    except ValueError as e:
        print(f"❌ Ошибка преобразования переменных: {e}")
        exit(1)

# Основная функция бота
async def main():
    # Проверяем переменные
    config = check_env_vars()
    print("✅ Все переменные окружения корректны")
    
    # Восстанавливаем сессию
    try:
        with open("my_account.session", "wb") as f:
            f.write(base64.b64decode(config['session_b64']))
        print("✅ Сессия успешно восстановлена")
    except Exception as e:
        print(f"❌ Ошибка восстановления сессии: {e}")
        exit(1)
    
    # Запускаем клиент
    app = Client(
        "my_account",
        api_id=config['api_id'],
        api_hash=config['api_hash'],
        workdir=".",
        in_memory=True
    )
    
    async with app:
        delay = 0
        while True:
            try:
                await app.send_message(
                    config['chat_id'],
                    f"⏰ Сообщение после {4*60 + delay} минут"
                )
                print(f"📨 Сообщение отправлено (задержка +{delay} минут)")
                
                await asyncio.sleep(4 * 3600 + delay * 60)
                delay = (delay + 1) % 60
            except Exception as e:
                print(f"⚠️ Ошибка: {e}. Повтор через 60 сек...")
                await asyncio.sleep(60)

if __name__ == "__main__":
    print("🚀 Запуск Telegram бота")
    asyncio.run(main())
