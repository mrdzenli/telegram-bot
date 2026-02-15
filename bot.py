import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== Настройки ======
TOKEN = "8313603481:AAF34DtYN0cDMMcY0vJsQgdNGH7reZdGZgI"
CHAT_ID = 800678838
PORT = int(os.environ.get("PORT", 5000))
URL = "https://имя_сервиса.bothost.ru"  # поменяй на публичный URL твоего проекта

# ====== Команда /start ======
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот подключен и работает через Webhook!")

# ====== Запуск Webhook ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))

    print(f"Bot starting with Webhook: {URL}/{TOKEN} on port {PORT}")
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"{URL}/{TOKEN}"
    )
