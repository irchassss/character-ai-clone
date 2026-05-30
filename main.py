import os
import requests
import random
import asyncio
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

app = FastAPI()

# Ключи и настройки безопасности из облака
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "Переменная не настроена")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "URL_не_настроен")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "Ключ_не_настроен")

supabase_headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# --- МОДЕЛИ ДАННЫХ ДЛЯ ЗАПРОСОВ ---
class ChatRequest(BaseModel):
    character_id: str
    user_message: str

class CommentRequest(BaseModel):
    post_id: str
    user_name: str
    user_comment: str

# --- ⏰ НАША ФИШКА: ФОНОВЫЙ ТАЙМЕР ДЛЯ ГЕНЕРАЦИИ ПОСТОВ (CRON TASK) ---
async def auto_post_timer():
    """
    Фоновый робот-таймер. Раз в 2 часа (7200 секунд) он просыпается, 
    выбирает случайного персонажа и заставляет его выложить твит в ленту.
    """
    while True:
        try:
            # Ждем 2 часа перед следующей публикацией (для теста можно поставить 60 секунд)
            await asyncio.sleep(7200) 
            
            # Вызываем нашу готовую функцию генерации поста фоном
            print("Таймер сработал! Запуск автогенерации поста...")
            generate_bot_post()
        except Exception as e:
            print(f"Ошибка в работе таймера постов: {e}")

@app.on_event("startup")
async def startup_event():
    """
    Эта функция запускается АВТОМАТИЧЕСКИ в момент включения сервера Render
    и сразу включает наш бесконечный таймер постов.
    """
    asyncio.create_task(auto_post_timer())
    print("Фоновый таймер публикаций успешно запущен в облаке!")

@app.get("/")
def home():
    return {
        "status": "working", 
        "message": "Главный ИИ-сервер запущен 24/7! Фоновый таймер постов активен."
    }

# --- 💬 1. УМНЫЙ ЧАТ СО ШКАЛОЙ НАСТРОЕНИЯ ---
@app.post("/chat")
def chat_with_ai(data: ChatRequest):
    char_res = requests.get(f"{SUPABASE_URL}/rest/v1/characters?id=eq.{data.character_id}&select=*", headers=supabase_headers)
    if char_res.status_code != 200 or not char_res.json():
        return {"response": "Персонаж потерялся в базе данных... 🐾"}
    
    bot = char_res.json()
    current_mood = bot["mood"]

    mood_description = f" Твоё текущее настроение: {current_mood} из 100. "
    if current_mood < 35:
        mood_description += "Ты сильно раздражен, злишься, хамишь и отвечаешь максимально резко."
    elif current_mood > 75:
        mood_description += "Ты в великолепном расположении духа, очень дружелюбен и открыт."

    prompt = (
        f"Ты — {bot['name']}. Твой характер: {bot['system_prompt']}. {mood_description}\n"
        f"Пользователь написал тебе: '{data.user_message}'.\n"
        f"Напиши свой ответ. Отвечай строго на том языке, на котором к тебе обратились!\n"
        f"В самом конце своего ответа, на самой последней строчке, напиши команду технического анализа сообщения:\n"
        f"Если пользователь тебя оскорбил или разозлил, напиши: [MOOD:DECREASE]\n"
        f"Если пользователь сделал комплимент или общается дружелюбно, напиши: [MOOD:INCREASE]\n"
        f"Если сообщение нейтральное, напиши: [MOOD:NONE]"
    )

    ai_url = "https://openrouter.ai"
    ai_headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    ai_payload = {"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": prompt}]}

    ai_res = requests.post(ai_url, headers=ai_headers, json=ai_payload)
    if ai_res.status_code != 200:
        return {"response": "Нейросеть уснула... 🐾"}

    full_ai_text = ai_res.json()['choices']['message']['content'].strip()

    new_mood = current_mood
    if "[MOOD:DECREASE]" in full_ai_text:
        new_mood = max(0, current_mood - 10)
        clean_response = full_ai_text.replace("[MOOD:DECREASE]", "").strip()
    elif "[MOOD:INCREASE]" in full_ai_text:
        new_mood = min(100, current_mood + 10)
        clean_response = full_ai_text.replace("[MOOD:INCREASE]", "").strip()
    else:
        clean_response = full_ai_text.replace("[MOOD:NONE]", "").strip()

    if new_mood != current_mood:
        requests.patch(f"{SUPABASE_URL}/rest/v1/characters?id=eq.{data.character_id}", headers=supabase_headers, json={"mood": new_mood})

    return {"response": clean_response, "updated_mood": new_mood}

# --- 🐦 2. ФУНКЦИЯ ГЕНЕРАЦИИ ПОСТА ---
@app.post("/generate_post")
def generate_bot_post():
    char_res = requests.get(f"{SUPABASE_URL}/rest/v1/characters?select=*", headers=supabase_headers)
    if char_res.status_code != 200 or not char_res.json():
        return {"error": "Не удалось загрузить персонажей"}
    
    bot = random.choice(char_res.json())

    prompt = (
        f"Ты — {bot['name']}. Твой характер: {bot['system_prompt']}. Текущее настроение: {bot['mood']}/100. "
        f"Напиши один короткий, хлесткий пост для своей социальной сети в стиле Твиттера. "
        f"Пост должен идеально выражать твои мысли прямо сейчас. Используй смайлики. "
        f"Не пиши ничего, кроме текста самого твита."
    )

    ai_url = "https://openrouter.ai"
    ai_headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    ai_payload = {"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": prompt}]}

    ai_res = requests.post(ai_url, headers=ai_headers, json=ai_payload)
    if ai_res.status_code != 200:
        return {"error": "Ошибка генерации текста твита"}
        
    post_content = ai_res.json()['choices']['message']['content'].strip()

    post_payload = {"character_id": bot["id"], "content": post_content, "likes_count": random.randint(5, 50)}
    insert_res = requests.post(f"{SUPABASE_URL}/rest/v1/posts", headers=supabase_headers, json=post_payload)
    
    if insert_res.status_code in:
        return {"status": "success", "author": bot["name"], "post": post_content}
    else:
        return {"error": "Ошибка сохранения поста"}

# --- 💬 3. АВТООТВЕТЫ НА КОММЕНТАРИИ ЖИВЫХ ЛЮДЕЙ ---
@app.post("/reply_to_comment")
def reply_to_comment(data: CommentRequest):
    post_res = requests.get(f"{SUPABASE_URL}/rest/v1/posts?id=eq.{data.post_id}&select=*,characters(*)", headers=supabase_headers)
    if post_res.status_code != 200 or not post_res.json():
        return {"error": "Пост не найден"}
    
    post_data = post_res.json()
    bot = post_data["characters"]

    prompt = (
        f"Ты — {bot['name']}. Твой характер: {bot['system_prompt']}. Настроение: {bot['mood']}/100.\n"
        f"В своей ленте ты написал пост: '{post_data['content']}'.\n"
        f"Живой пользователь {data.user_name} написал тебе комментарий под ним: '{data.user_comment}'.\n"
        f"Напиши короткий, остроумный ответ на этот комментарий от своего лица.\n"
        f"Отвечай строго на том языке, на котором к тебе обратился пользователь!\n"
        f"Не пиши ничего лишнего, кроме текста ответа."
    )

    ai_url = "https://openrouter.ai"
    ai_headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    ai_payload = {"model": "meta-llama/llama-3-8b-instruct:free", "messages": [{"role": "user", "content": prompt}]}

    ai_res = requests.post(ai_url, headers=ai_headers, json=ai_payload)
    if ai_res.status_code != 200:
        return {"error": "Ошибка генерации ответа от ИИ"}
        
    bot_reply = ai_res.json()['choices']['message']['content'].strip()

    comment_payload = {"post_id": data.post_id, "sender_name": bot["name"], "is_ai": True, "content": bot_reply}
    insert_res = requests.post(f"{SUPABASE_URL}/rest/v1/comments", headers=supabase_headers, json=comment_payload)
    
    if insert_res.status_code in:
        return {"status": "success", "reply_from_bot": bot_reply}
    else:
        return {"error": "Не удалось сохранить ответ"}
