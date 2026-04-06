import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

users = {}

keyboard = [
    ["➕ Стол", "🍰 Десерт"],
    ["📊 Статистика", "🏆 Рейтинг"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.effective_user.first_name

    if user_id not in users:
        users[user_id] = {
            "name": name,
            "tables": 0,
            "desserts": 0
        }

    await update.message.reply_text(f"{name}, ты подключен ✅", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in users:
        return

    text = update.message.text

    if text == "➕ Стол":
        users[user_id]["tables"] += 1
        await update.message.reply_text("Стол добавлен ✅")

    elif text == "🍰 Десерт":
        users[user_id]["desserts"] += 1
        await update.message.reply_text("Десерт добавлен ✅")

    elif text == "📊 Статистика":
        data = users[user_id]
        tables = data["tables"]
        desserts = data["desserts"]

        percent = (desserts / tables * 100) if tables > 0 else 0
        left = tables - desserts

        await update.message.reply_text(
            f"📊 {data['name']}\n"
            f"Столы: {tables}\n"
            f"Десерты: {desserts}\n"
            f"Конверсия: {percent:.0f}%\n"
            f"До 100%: {left}"
        )

    elif text == "🏆 Рейтинг":
        ranking = []

        for user in users.values():
            tables = user["tables"]
            desserts = user["desserts"]
            percent = (desserts / tables * 100) if tables > 0 else 0
            ranking.append((user["name"], percent))

        ranking.sort(key=lambda x: x[1], reverse=True)

        text = "🏆 Рейтинг:\n"
        for i, (name, percent) in enumerate(ranking[:5], start=1):
            text += f"{i}. {name} — {percent:.0f}%\n"

        await update.message.reply_text(text)

TOKEN = os.getenv("BOT_TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("Bot started...")
    app.run_polling()
