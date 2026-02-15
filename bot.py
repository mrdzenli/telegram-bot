from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== Настройки бота ======
TOKEN = "8313603481:AAF34DtYN0cDMMcY0vJsQgdNGH7reZdGZgI"
CHAT_ID = 800678838  # твой чат ID

# ====== Команда /start ======
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот подключен и работает!")

# ====== Запуск приложения ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))

    print("Bot is starting...")
    app.run_polling()
