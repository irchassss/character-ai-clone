import os
import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "Переменная не настроена")

# Модель данных, которую будет присылать планшет/телефон
class ChatRequest(BaseModel):
    character_name: str
    system_prompt: str
    current_mood: int
    user_message: str

@app.get("/")
def home():
    return {"status": "working", "message": "ИИ-сервер Клона Character.ai запущен и готов к работе 24/7!"}

@app.post("/chat")
def chat_with_ai(data: ChatRequest):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    mood_description = f" Твоё текущее настроение: {data.current_mood} из 100. "
    if data.current_mood < 40:
        mood_description += "Ты очень раздражен, злишься и отвечаешь резко."
    elif data.current_mood > 70:
        mood_description += "Ты в отличном расположении духа, более дружелюбен, чем обычно."
    
    full_system_prompt = data.system_prompt + mood_description

    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": data.user_message}
        ]
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        ai_response = response.json()['choices']['message']['content']
        return {"response": ai_response}
    else:
        return {"response": f"Ошибка связи с ИИ. Статус: {response.status_code}"}
