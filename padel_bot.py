import asyncio
import logging
import os
from datetime import datetime, time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Токен берем из переменных окружения Render
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Укажем ваш ID в Render, чтобы уведомления приходили сразу

# Целевые дни: Вторник (1), Среда (2), Четверг (3)
TARGET_DAYS = {1, 2, 3}
START_TIME_MIN = time(19, 0)       # После 19:00
ALLOWED_DURATIONS = {60, 90, 120}  # 1:00, 1:30, 2:00 в минутах


async def check_slots(app):
    """Функция проверки слотов каждые 10 минут."""
    target_chat_id = CHAT_ID
    if not target_chat_id:
        logging.info("CHAT_ID не задан. Напишите боту /start в Telegram.")
        return

    logging.info("Проверка свободных слотов...")

    # TODO: Здесь будет код запроса к вашему сайту бронирования.
    # Когда пришлете ссылку на сайт — настроим получение реальных данных.
    found_slots = [] 

    available_text = []
    for slot in found_slots:
        slot_date = datetime.strptime(slot["date"], "%Y-%m-%d")
        slot_time = datetime.strptime(slot["start"], "%H:%M").time()

        if (
            slot_date.weekday() in TARGET_DAYS
            and slot_time >= START_TIME_MIN
            and slot["duration"] in ALLOWED_DURATIONS
        ):
            hours = slot["duration"] // 60
            mins = slot["duration"] % 60
            dur_str = f"{hours}ч" + (f" {mins}мин" if mins else "")
            
            available_text.append(
                f"📅 **{slot['date']}** | ⏰ **{slot['start']}** ({dur_str})\n🔗 [Забронировать]({slot['url']})"
            )

    if available_text:
        message = "🎾 **Найдены свободные корты!**\n\n" + "\n\n".join(available_text)
        await app.bot.send_message(chat_id=target_chat_id, text=message, parse_mode="Markdown")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """При вызове /start бот запоминаетваш chat_id и присылает подтверждение."""
    global CHAT_ID
    CHAT_ID = str(update.effective_chat.id)
    logging.info(f"Получен CHAT_ID: {CHAT_ID}")
    await update.message.reply_text(
        f"Привет! Ваш ID ({CHAT_ID}) сохранен.\n"
        f"Я буду проверять слоты каждые 10 минут.\n"
        f"Параметры: Вт/Ср/Чт, после 19:00 (1:00, 1:30 или 2:00)."
    )


def main():
    if not BOT_TOKEN:
        raise ValueError("Ошибка: Не задана переменная BOT_TOKEN!")

    # Явное создание event loop для compatibility с новыми версиями Python
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    # Настройка планировщика проверки (каждые 10 минут)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_slots, 'interval', minutes=10, args=[app])
    scheduler.start()

    logging.info("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()
