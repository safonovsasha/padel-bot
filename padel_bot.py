#!/usr/bin/env python3
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8654397067:AAEtEXyAYp1jGZNuU21sL3WVaar-sgHe4Rs"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Падел-бот работает! 🎾")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
