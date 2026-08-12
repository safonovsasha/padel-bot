import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Падел-бот работает! 🎾\nВт-Чт после 19:00")

async def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("Ошибка: BOT_TOKEN не найден!")
        return
    
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
