from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# 🔐 ВСТАВЬ СЮДА ТОКЕН ОТ BOTFATHER
TOKEN = "YOUR_BOT_TOKEN"

questions = [
    ("Кто вам интереснее?", ["Только кошка", "Только собака", "Любой вариант"]),
    ("Есть ли аллергия?", ["Сильная", "Слабая", "Нет"]),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["step"] = 0
    context.user_data["answers"] = []
    await ask(update, context)

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    step = context.user_data["step"]
    question, options = questions[step]

    keyboard = [[o] for o in options]

    await update.message.reply_text(
        question,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    context.user_data["answers"].append(text)
    context.user_data["step"] += 1

    if context.user_data["step"] < len(questions):
        await ask(update, context)
    else:
        await result(update, context)

async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answers = context.user_data["answers"]

    if "Только кошка" in answers:
        text = "🐱 Тебе больше подойдёт кошка!"
    elif "Только собака" in answers:
        text = "🐶 Тебе больше подойдёт собака!"
    else:
        text = "🐾 Тебе подходят оба варианта!"

    await update.message.reply_text(text)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
