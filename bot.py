import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext,
)

# Конфигурация бота
TOKEN = """7927337290:AAEnfzGlXmm2KXVw3HwVRXYBZVd26UFrvgo"""
if not TOKEN:
    raise ValueError("Не установлен токен бота. Укажите его в переменных окружения.")

# Состояния дуэлей
duels = {}  # Формат: {chat_id: {message_id: {'attacker': user_id, 'defender': user_id, 'status': 'pending/active', 'turn': user_id}}}

def start(update: Update, context: CallbackContext) -> None:
    """Обработчик команды /start"""
    update.message.reply_text(
        "🐷 Добро пожаловать в Свинобойню! 🐷\n\n"
        "Чтобы вызвать кого-то на свинобойню, ответьте на его сообщение текстом 'свинобой'"
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработчик обычных сообщений"""
    if update.message.reply_to_message and update.message.text.lower() == 'свинобой':
        # Кто-то вызывает на дуэль
        start_duel(update, context)

def start_duel(update: Update, context: CallbackContext) -> None:
    """Начало дуэли"""
    chat_id = update.message.chat_id
    attacker = update.message.from_user
    defender = update.message.reply_to_message.from_user
    
    # Проверка на самовызов
    if attacker.id == defender.id:
        update.message.reply_text("Нельзя вызвать самого себя на свинобойню!")
        return
    
    message_id = update.message.reply_to_message.message_id
    
    # Проверка на уже существующую дуэль
    if chat_id in duels and message_id in duels[chat_id]:
        update.message.reply_text("Свинобойня уже началась с этим сообщением!")
        return
    
    # Создаем запись о дуэли
    if chat_id not in duels:
        duels[chat_id] = {}
    
    duels[chat_id][message_id] = {
        'attacker': attacker,
        'defender': defender,
        'status': 'pending',
        'turn': None
    }
    
    # Удаляем сообщение "свинобой"
    context.bot.delete_message(chat_id, update.message.message_id)
    
    # Отправляем предложение дуэли
    keyboard = [
        [InlineKeyboardButton("Да, хочу хрюкать!", callback_data=f"duel_accept_{message_id}")],
        [InlineKeyboardButton("Нет, я не свинья!", callback_data=f"duel_decline_{message_id}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=chat_id,
        reply_to_message_id=message_id,
        text=f"🐷 {defender.first_name}, {attacker.first_name} вызывает вас на свинобойню! Примете вызов?",
        reply_markup=reply_markup
    )

def handle_duel_response(update: Update, context: CallbackContext) -> None:
    """Обработчик ответа на предложение дуэли"""
    query = update.callback_query
    query.answer()
    
    chat_id = query.message.chat_id
    message_id = int(query.data.split('_')[-1])
    
    # Проверяем существование дуэли
    if chat_id not in duels or message_id not in duels[chat_id]:
        query.edit_message_text("Эта свинобойня уже закончилась или отменена.")
        return
    
    duel = duels[chat_id][message_id]
    
    if query.data.startswith('duel_accept'):
        # Пользователь принял дуэль
        duel['status'] = 'active'
        duel['turn'] = duel['attacker'].id  # Первым ходит атакующий
        
        # Редактируем сообщение
        query.edit_message_text(
            f"🐷 {duel['defender'].first_name} согласился, и начинается свинобойня!\n\n"
            f"Первым хрюкает {duel['attacker'].first_name}!"
        )
        
        # Отправляем кнопки для дуэли
        send_duel_buttons(context, chat_id, message_id, duel['attacker'].id)
        
    elif query.data.startswith('duel_decline'):
        # Пользователь отказался от дуэли
        query.edit_message_text(
            f"🐷 {duel['defender'].first_name} отказался похрюкаться...\n"
            f"{duel['attacker'].first_name}, попробуйте найти другого соперника!"
        )
        del duels[chat_id][message_id]

def send_duel_buttons(context: CallbackContext, chat_id: int, message_id: int, user_id: int):
    """Отправляет кнопки для хода в дуэли"""
    duel = duels[chat_id][message_id]
    current_player = duel['attacker'] if user_id == duel['attacker'].id else duel['defender']
    opponent = duel['defender'] if user_id == duel['attacker'].id else duel['attacker']
    
    keyboard = [
        [InlineKeyboardButton("🐷 ХРЮ", callback_data=f"action_hryu_{message_id}")],
        [
            InlineKeyboardButton("🧶 ПОЧЁС", callback_data=f"action_scratch_{message_id}"),
            InlineKeyboardButton("🌀 УКЛОН", callback_data=f"action_dodge_{message_id}")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    context.bot.send_message(
        chat_id=chat_id,
        text=f"🐷 Ход {current_player.first_name} против {opponent.first_name}!",
        reply_markup=reply_markup
    )

def handle_duel_action(update: Update, context: CallbackContext) -> None:
    """Обработчик действий в дуэли"""
    query = update.callback_query
    query.answer()
    
    chat_id = query.message.chat_id
    message_id = int(query.data.split('_')[-1])
    action = query.data.split('_')[1]
    
    # Проверяем существование дуэли
    if chat_id not in duels or message_id not in duels[chat_id]:
        query.edit_message_text("Эта свинобойня уже закончилась.")
        return
    
    duel = duels[chat_id][message_id]
    
    # Проверяем, что ход делает правильный игрок
    current_user = query.from_user
    if current_user.id != duel['turn']:
        query.answer("Сейчас не ваш ход!", show_alert=True)
        return
    
    # Удаляем предыдущие кнопки
    context.bot.delete_message(chat_id, query.message.message_id)
    
    # Обрабатываем действие
    if action == 'hryu':
        # Обычный хрюк
        chance = 6
        success = random.randint(1, 100) <= chance
        if success:
            # Победа
            winner = current_user
            loser = duel['defender'] if current_user.id == duel['attacker'].id else duel['attacker']
            context.bot.send_message(
                chat_id=chat_id,
                text=f"🐷 {current_user.first_name} захрюкал {loser.first_name} ДО СМЕРТИ! {winner.first_name} победил в свинобойне! 🎉"
            )
            del duels[chat_id][message_id]
            return
        else:
            # Продолжаем дуэль
            context.bot.send_message(
                chat_id=chat_id,
                text=f"🐷 {current_user.first_name} хрюкнул, но {duel['defender'].first_name if current_user.id == duel['attacker'].id else duel['attacker'].first_name} выстоял!"
            )
    
    elif action == 'scratch':
        # Почесаться - увеличивает шанс на победу в следующем ходу
        context.bot.send_message(
            chat_id=chat_id,
            text=f"🧶 {current_user.first_name} почесался! Теперь его следующий хрюк будет с шансом 14% на победу!"
        )
    
    elif action == 'dodge':
        # Уклонение - уменьшает шанс противника
        context.bot.send_message(
            chat_id=chat_id,
            text=f"🌀 {current_user.first_name} уклонился! Теперь шанс противника хрюкнуть его до смерти снижен до 1%!"
        )
    
    # Меняем ход
    duel['turn'] = duel['defender'].id if duel['turn'] == duel['attacker'].id else duel['attacker'].id
    
    # Отправляем кнопки для следующего хода
    send_duel_buttons(context, chat_id, message_id, duel['turn'])

def main() -> None:
    """Запуск бота"""
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Обработчики сообщений
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Обработчики callback-запросов
    dispatcher.add_handler(CallbackQueryHandler(handle_duel_response, pattern='^duel_(accept|decline)'))
    dispatcher.add_handler(CallbackQueryHandler(handle_duel_action, pattern='^action_(hryu|scratch|dodge)'))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
