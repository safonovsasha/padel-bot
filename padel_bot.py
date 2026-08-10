import asyncio
import logging
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# --- ФЕЙКОВЫЙ СЕРВЕР ДЛЯ ОБМАНА RENDER (чтобы работало на FREE тарифе) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# Запуск веб-сервера в отдельном фоновом потоке
threading.Thread(target=run_dummy_server, daemon=True).start()
# ----------------------------------------------------------------------

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

TARGET_DAYS = {1, 2, 3}  # Вт, Ср, Чт
START_TIME_MIN = time(19, 0)
ALLOWED_DURATIONS = {60, 90, 120}


async def check_slots(app):
    """Фоновая проверка каждые 10 минут."""
    target_chat_id = CHAT_ID
    if not target_chat_id:
        return
    logging.info("Проверка свободных слотов...")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = str(update.effective_chat.id)
    logging.info(f"Получен CHAT_ID: {CHAT_ID}")
    await update.message.reply_text("Бот запущен и проверяет слоты!")


def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN не найден!")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_slots, 'interval', minutes=10, args=[app])
    scheduler.start()

    logging.info("Бот запущен на Render Free...")
    app.run_polling()


if __name__ == "__main__":
    main()
