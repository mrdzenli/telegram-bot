import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, Dispatcher

# ====== Переменные окружения ======
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID", "0"))
PORT = int(os.environ.get("PORT", 5000))  # BotHost даёт порт через переменную
URL = os.environ.get("BOT_URL")  # твой публичный URL, например https://имя_сервиса.bothost.ru

if not TOKEN or not CHAT_ID or not URL:
    print("ERROR: Проверь BOT_TOKEN, CHAT_ID и BOT_URL")
    exit(1)

# ====== Команда /start ======
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот подключен и работает!")

# ====== Запуск приложения с Webhook ======
if __name__ == "__main__":
    # Создаём приложение
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))

    # Запуск Webhook
    print(f"Bot starting with Webhook: {URL}/{TOKEN} on port {PORT}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,            # путь webhook
        webhook_url=f"{URL}/{TOKEN}"
    )
