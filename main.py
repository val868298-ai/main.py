from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [
                    {
                        "role": "system",
                        "content": "Ты дружелюбный учитель корейского языка."
                    },
                    {
                        "role": "user",
                        "content": user_text
                    }
                ]
            }
        )

        data = response.json()

        if response.status_code != 200:
            answer = f"HTTP error: {data}"
        elif "error" in data:
            answer = data["error"]["message"]
        else:
            answer = data["choices"][0]["message"]["content"]

        await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(str(e))


app = Application.builder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))
app.run_polling()
