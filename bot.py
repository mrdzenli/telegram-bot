import os
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

print("=== DEBUG: Starting bot ===")

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID_ENV = os.getenv("CHAT_ID")
print(f"DEBUG: BOT_TOKEN={TOKEN}")
print(f"DEBUG: CHAT_ID={CHAT_ID_ENV}")

if not TOKEN or not CHAT_ID_ENV:
    print("ERROR: BOT_TOKEN или CHAT_ID не заданы!")
    sys.exit(1)

try:
    CHAT_ID = int(CHAT_ID_ENV)
except ValueError:
    print(f"ERROR: CHAT_ID не число: {CHAT_ID_ENV}")
    sys.exit(1)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот подключен и работает!")

if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start_command))
        print("=== DEBUG: Running polling ===")
        app.run_polling()
    except Exception as e:
        print("ERROR during bot startup:", e)
        sys.exit(1)
