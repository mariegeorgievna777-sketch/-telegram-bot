
# Online Python - IDE, Editor, Compiler, Interpreter

def sum(a, b):
    return (a + b)

a = int(input('Enter 1st number: '))
b = int(input('Enter 2nd number: '))

print(f'Sum of {a} and {b} is {sum(a, b)}')
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "Identify_your_animal_bot"

questions = [
    ("Кто вам интереснее?", ["Только кошка", "Только собака", "Любой вариант"]),
    ("Есть ли аллергия?", ["Сильная", "Слабая", "Нет"]),
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["step"] = 0
    context.user_data["answers"] = []
    await ask(update, context)

async def ask(update, context):
    step = context.user_data["step"]
    q, options = questions[step]
    keyboard = [[o] for o in options]
    await update.message.reply_text(q, reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["answers"].append(update.message.text)
    context.user_data["step"] += 1

    if context.user_data["step"] < len(questions):
        await ask(update, context)
    else:
        await result(update, context)

async def result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answers = context.user_data["answers"]

    if "Только кошка" in answers:
        text = "Тебе подойдёт кошка 🐱"
    elif "Только собака" in answers:
        text = "Тебе подойдёт собака 🐶"
    else:
        text = "Тебе подходят оба варианта 🐾"

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle))

app.run_polling()