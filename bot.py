import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ====== Настройки ======
import os

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
words_file = "words.txt"      # файл со словами
periodic_job = None

# ====== Загрузка слов ======
try:
    with open(words_file, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    words = []

# ====== Клавиатура Старт/Стоп ======
def get_keyboard():
    keyboard = [
        [InlineKeyboardButton("Старт", callback_data="start")],
        [InlineKeyboardButton("Стоп", callback_data="stop")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====== Команда /start ======
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Используй кнопки для управления сообщениями.\n\n"
        "Команды:\n"
        "/add слово — добавить слово\n"
        "/remove слово — удалить слово\n"
        "/list — показать все слова\n"
        "/clear — очистить список слов",
        reply_markup=get_keyboard()
    )

# ====== Добавление слова ======
async def add_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global words
    if context.args:
        new_word = " ".join(context.args)
        words.append(new_word)
        with open(words_file, "a", encoding="utf-8") as f:
            f.write(new_word + "\n")
        await update.message.reply_text(f"✅ Слово добавлено: {new_word}")
    else:
        await update.message.reply_text("Используй: /add слово")

# ====== Удаление слова ======
async def remove_word(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global words
    if context.args:
        word_to_remove = " ".join(context.args)
        if word_to_remove in words:
            words.remove(word_to_remove)
            with open(words_file, "w", encoding="utf-8") as f:
                for w in words:
                    f.write(w + "\n")
            await update.message.reply_text(f"❌ Слово удалено: {word_to_remove}")
        else:
            await update.message.reply_text("⚠️ Такого слова нет в списке.")
    else:
        await update.message.reply_text("Используй: /remove слово")

# ====== Показ списка слов ======
async def list_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if words:
        await update.message.reply_text("📚 Слова:\n" + "\n".join(words))
    else:
        await update.message.reply_text("Список пустой.")

# ====== Очистка всего списка ======
async def clear_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global words
    words = []
    with open(words_file, "w", encoding="utf-8") as f:
        f.write("")
    await update.message.reply_text("🗑️ Список слов очищен полностью.")

# ====== Периодическое сообщение ======
async def periodic_message(context: ContextTypes.DEFAULT_TYPE):
    if words:
        word = random.choice(words)
        await context.bot.send_message(chat_id=CHAT_ID, text=f"📌 {word}")
    else:
        await context.bot.send_message(chat_id=CHAT_ID, text="Список слов пустой. Добавь новые через /add")

# ====== Кнопки Старт/Стоп ======
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global periodic_job
    query = update.callback_query
    await query.answer()
    if query.data == "start":
        if periodic_job is None:
            periodic_job = context.job_queue.run_repeating(periodic_message, interval=1800, first=10)
            await query.edit_message_text("Сообщения включены ✅", reply_markup=get_keyboard())
        else:
            await query.edit_message_text("Сообщения уже запущены ⚠️", reply_markup=get_keyboard())
    elif query.data == "stop":
        if periodic_job is not None:
            periodic_job.schedule_removal()
            periodic_job = None
            await query.edit_message_text("Сообщения остановлены ❌", reply_markup=get_keyboard())
        else:
            await query.edit_message_text("Сообщения уже остановлены ⚠️", reply_markup=get_keyboard())

# ====== Запуск бота ======
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("add", add_word))
    app.add_handler(CommandHandler("remove", remove_word))
    app.add_handler(CommandHandler("list", list_words))
    app.add_handler(CommandHandler("clear", clear_words))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()