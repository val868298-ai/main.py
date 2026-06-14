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
                "content": "Ты дружелюбный собеседник, который помогает учить корейский язык."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }
)

data = response.json()

# 👇 ВАЖНО: сначала проверяем ошибку
if "error" in data:
    answer = f"API error: {data['error']['message']}"
else:
    answer = data["choices"][0]["message"]["content"]

await update.message.reply_text(answer)
