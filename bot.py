import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ====== Дебаг переменных окружения ======
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_ENV = os.getenv("CHAT_ID")

print("=== DEBUG: Starting minimal bot ===")
print(f"DEBUG: BOT_TOKEN={TOKEN}")
print(f"DEBUG: CHAT_ID_ENV={CHAT_ID_ENV}")

if not TOKEN or not CHAT_ID_ENV:
    print("ERROR: BOT_TOKEN или CHAT_ID не задан!")
    sys.exit(1)

try:
    CHAT_ID = int(CHAT_ID_ENV)
except ValueError:
    print(f"ERROR: CHAT_ID не число: {CHAT_ID_ENV}")
    sys.exit(1)

print("=== DEBUG: Environment variables are OK ===")

# ====== Команда /start ======
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот подключен и работает!")

# ====== Запуск бота ======
if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start_command))
        print("=== DEBUG: Starting polling ===")
        app.run_polling()
    except Exception as e:
        print("ERROR during bot startup:", e)
        sys.exit(1)
