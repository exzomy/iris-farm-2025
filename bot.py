# generate_session.py
from pyrogram import Client

print("Создаем session-файл...")
Client(
    "my_account",  # Будет создан my_account.session
    api_id=1234567,  # Ваш API_ID
    api_hash="ваш_api_hash"  # Ваш API_HASH
).start()

