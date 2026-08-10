from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8654397067:AAEtEXyAYp1jGZNuU21sL3WVaar-sgHe4Rs"

USER_DATA = {
    "name": "Сафонов Александр Юрьевич",
    "phone": "+79853452555",
    "email": "aysafonov@mail.ru",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Привет! Это падел-бот.\n\nВт-Чт после 19:00"
    keyboard = [[InlineKeyboardButton("На сайт", url="https://outdoor.sport.mos.ru")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
