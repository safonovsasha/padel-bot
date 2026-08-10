
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime
import asyncio

USER_DATA = {
    "name": "Сафонов Александр Юрьевич",
    "email": "aysafonov@mail.ru",
    "phone": "+79853452555",
    "participants": 2,
    "duration_preference": "90-120 минут",
    "days_preference": "Вт, Ср, Чт",
    "time_preference": "после 19:00"
}

TOKEN = "8654397067:AAEtEXyAYp1jGZNuU21sL3WVaar-sgHe4Rs"
CHECK_INTERVAL = 600
is_checking = False
chat_id = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global chat_id
    chat_id = update.effective_chat.id
    
    text = f"Привет, {USER_DATA['name'].split()[1]}!\n\n"
    text += "Бот для поиска слотов на падел.\n\n"
    text += f"Дни: {USER_DATA['days_preference']}\n"
    text += f"Время: {USER_DATA['time_preference']}\n"
    text += f"Длительность: {USER_DATA['duration_preference']}\n"
    
    keyboard = [
        [InlineKeyboardButton("🔍 Начать проверку", callback_data="start_check")],
        [InlineKeyboardButton("🔗 На сайт", url="https://outdoor.sport.mos.ru/#venues-events")],
        [InlineKeyboardButton("📋 Данные", callback_data="my_data")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup)

async def check_slots_loop(context):
    global is_checking, chat_id
    
    while is_checking and chat_id:
        try:
            now = datetime.now().strftime("%H:%M")
            text = f"🔍 {now}\n"
            text += f"Ищу: {USER_DATA['days_preference']} после {USER_DATA['time_preference']}\n"
            text += "Запись открывается на 3 дня вперед 🎾"
            
            keyboard = [[InlineKeyboardButton("На сайт", url="https://outdoor.sport.mos.ru/#venues-events")]]
            
            await context.bot.send_message(chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(keyboard))
            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(60)

async def start_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_checking
    query = update.callback_query
    await query.answer()
    is_checking = True
    
    text = f"✅ Проверка каждые {CHECK_INTERVAL//60} мин\n"
    text += f"Ищу: {USER_DATA['days_preference']}\n"
    text += f"Время: {USER_DATA['time_preference']}"
    
    asyncio.create_task(check_slots_loop(context))
    
    keyboard = [[InlineKeyboardButton("⏹️ Стоп", callback_data="stop_check")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def stop_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_checking
    query = update.callback_query
    await query.answer()
    is_checking = False
    
    text = "⏹️ Проверка остановлена"
    keyboard = [[InlineKeyboardButton("🔍 Начать", callback_data="start_check")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def my_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = f"ФИО: {USER_DATA['name']}\n"
    text += f"Тел: {USER_DATA['phone']}\n"
    text += f"Email: {USER_DATA['email']}\n\n"
    text += f"Дни: {USER_DATA['days_preference']}\n"
    text += f"Время: {USER_DATA['time_preference']}\n"
    text += f"Длительность: {USER_DATA['duration_preference']}"
    
    keyboard = [[InlineKeyboardButton("Назад", callback_data="back")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    text = f"Привет, {USER_DATA['name'].split()[1]}!\n\n"
    text += f"Дни: {USER_DATA['days_preference']}\n"
    text += f"Время: {USER_DATA['time_preference']}\n"
    
    keyboard = [
        [InlineKeyboardButton("🔍 Начать", callback_data="start_check")],
        [InlineKeyboardButton("🔗 На сайт", url="https://outdoor.sport.mos.ru/#venues-events")],
        [InlineKeyboardButton("📋 Данные", callback_data="my_data")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

def main():
    print("🤖 Падел-бот запущен!")
    print(f"Проверка каждые {CHECK_INTERVAL//60} мин")
    
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start_check, pattern="^start_check$"))
    app.add_handler(CallbackQueryHandler(stop_check, pattern="^stop_check$"))
    app.add_handler(CallbackQueryHandler(my_data, pattern="^my_data$"))
    app.add_handler(CallbackQueryHandler(back, pattern="^back$"))
    
    app.run_polling()

if __name__ == "__main__":
    main()
EOF
