from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

# берём ключи из Railway (Variables)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "system",
                    "content": "Ты дружелюбный собеседник, который помогает учить корейский язык. Отвечай на корейском просто и естественно."
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        )

        await update.message.reply_text(response.output_text)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
