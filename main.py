import os
import requests

# GitHub больше не будет ругаться! Ключ подтянется из настроек сервера безопасности
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "Переменная не настроена")

def generate_ai_response(character_name, system_prompt, current_mood, user_message):
    url = "https://openrouter.ai"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Динамически меняем поведение ИИ в зависимости от нашей фишки — шкалы настроения
    mood_description = f" Твоё текущее настроение: {current_mood} из 100. "
    if current_mood < 40:
        mood_description += "Ты очень раздражен, злишься и отвечаешь резко."
    elif current_mood > 70:
        mood_description += "Ты в отличном расположении духа, более дружелюбен, чем обычно."
    
    full_system_prompt = system_prompt + mood_description

    # Используем отличную и полностью бесплатную модель Llama 3
    data = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": full_system_prompt},
            {"role": "user", "content": user_message}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices']['message']['content']
    else:
        return f"Ошибка API: {response.status_code}. Кот ушёл спать... 🐾"

if __name__ == "__main__":
    print("ИИ-модуль character-ai-clone готов к работе в облаке!")
