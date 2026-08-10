#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from datetime import datetime

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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"Привет!\n\n"
    text += f"Дни: {USER_DATA['days_preference']}\n"
    text += f"Время: {USER_DATA['time_preference']}\n"
    
    keyboard = [
        [InlineKeyboardButton("📋 Мои данные", callback_data="data")],
        [InlineKeyboardButton("🔗 На сайт", url="https://outdoor.sport.mos.ru/#venues-events")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "data":
        text = f"ФИО: {USER_DATA['name']}\n"
        text += f"Тел: {USER_DATA['phone']}\n"
        text += f"Email: {USER_DATA['email']}\n\n"
        text += f"Дни: {USER_DATA['days_preference']}\n"
        text +=
