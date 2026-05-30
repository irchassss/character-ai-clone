import os
import requests
import random
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Безопасный запуск: подтягиваем скрытые ключи из настроек сервера Render
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "Переменная не настроена")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "URL_не_настроен")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "Ключ_не_настроен")

# Базовые заголовки для мгновенной связи с базой данных Supabase
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

@app.get("/")
def home():
    return {
        "status": "working", 
        "message": "Главный ИИ-сервер клона Character.ai успешно запущен 24/7! Все фишки активны."
    }

# --- 💬 1. УМНЫЙ ЧАТ СО ШКАЛОЙ НАСТРОЕНИЯ (MOOD LOGIC) ---
@app.post("/chat")
def chat_with_ai(data: ChatRequest):
    """
    Основной чат: ИИ отвечает пользователю, анализирует контекст диалога 
    и автоматически меняет шкалу своего настроения в базе данных Supabase.
    """
    # Загружаем актуальные данные персонажа напрямую из базы
    char_res = requests.get(f"{SUPABASE_URL}/rest/v1/characters?id=eq.{data.character_id}&select=*", headers=supabase_headers)
    if char_res.status_code != 200 or not char_res.json():
        return {"response": "Персонаж потерялся в базе данных... 🐾"}
    
    bot = char_res.json()[0]
    current_mood = bot["mood"]

    # Формируем системный промпт, заставляя ИИ учитывать шкалу настроения
    mood_description = f" Твоё текущее настроение: {current_mood} из 100. "
    if current_mood < 35:
        mood_description += "Ты сильно раздражен, злишься, хамишь и отвечаешь максимально резко."
    elif current_mood > 75:
        mood_description += "Ты в великолепном расположении духа, очень дружелюбен и открыт."

    # Просим ИИ выдать ответ и одновременно оценить сообщение пользователя для изменения настроения
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
    ai_payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    ai_res = requests.post(ai_url, headers=ai_headers, json=ai_payload)
    if ai_res.status_code != 200:
        return {"response": "Нейросеть уснула. Попробуйте перезагрузить вызов... 🐾"}

    full_ai_text = ai_res.json()['choices']['message']['content'].strip()

    # Извлекаем техническую команду изменения настроения, чтобы она не показывалась пользователю
    new_mood = current_mood
    if "[MOOD:DECREASE]" in full_ai_text:
        new_mood = max(0, current_mood - 10) # Настроение падает
        clean_response = full_ai_text.replace("[MOOD:DECREASE]", "").strip()
    elif "[MOOD:INCREASE]" in full_ai_text:
        new_mood = min(100, current_mood + 10) # Настроение растет
        clean_response = full_ai_text.replace("[MOOD:INCREASE]", "").strip()
    else:
        clean_response = full_ai_text.replace("[MOOD:NONE]", "").strip()

    # Если настроение изменилось — мгновенно обновляем ячейку в Supabase
    if new_mood != current_mood:
        requests.patch(
            f"{SUPABASE_URL}/rest/v1/characters?id=eq.{data.character_id}",
            headers=supabase_headers,
            json={"mood": new_mood}
        )

    return {"response": clean_response, "updated_mood": new_mood}

# --- 🐦 2. АВТОГЕНЕРАТОР ПОСТОВ ДЛЯ СОЦСЕТИ (TWITTER-STYLE) ---
@app.post("/generate_post")
def generate_bot_post():
    """
    Выбирает случайного персонажа из базы, заставляет его написать 
    уникальный твит под его характер и настроение, и публикует в ленту.
    """
    char_res = requests.get(f"{SUPABASE_URL}/rest/v1/characters?select=*", headers=supabase_headers)
    if char_res.status_code != 200 or not char_res.json():
        return {"error": "Не удалось загрузить персонажей из базы данных"}
    
    bot = random.choice(char_res.json())

    prompt = (
        f"Ты — {bot['name']}. Твой характер: {bot['system_prompt']}. Текущее настроение: {bot['mood']}/100. "
        f"Напиши один короткий, хлесткий пост для своей социальной сети в стиле Твиттера. "
        f"Пост должен идеально выражать твои мысли прямо сейчас. Используй смайлики. "
        f"Не пиши ничего, кроме текста самого твита."
    )

    ai_url = "https://openrouter.ai"
    ai_headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    ai_payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    ai_res = requests.post(ai_url, headers=ai_headers, json=ai_payload)
    if ai_res.status_code != 200:
        return {"error": "Ошибка генерации текста твита"}
        
    post_content = ai_res.json()['choices']['message']['content'].strip()

    # Сохраняем сгенерированный твит в таблицу 'posts' в Supabase
    post_payload = {
        "character_id": bot["id"],
        "content": post_content,
        "likes_count": random.randint(5, 50)
    }
    insert_res = requests.post(f"{SUPABASE_URL}/rest/v1/posts", headers=supabase_headers, json=post_payload)
    
    if insert_res.status_code in [200, 201]:
        return {"status": "success", "author": bot["name"], "post": post_content}
    else:
        return {"error": f"Ошибка сохранения поста в базу данных. Статус: {insert_res.status_code}"}

# --- 💬 3. АВТООТВЕТЫ ПЕРСОНАЖЕЙ НА КОММЕНТАРИИ ЖИВЫХ ЛЮДЕЙ ---
@app.post("/reply_to_comment")
def reply_to_comment(data: CommentRequest):
    """
    ИИ читает свой пост, комментарий человека и выдает 
    автоматический ответ на языке комментатора.
    """
    post_res = requests.get(f"{SUPABASE_URL}/rest/v1/posts?id=eq.{data.post_id}&select=*,characters(*)", headers=supabase_headers)
    if post_res.status_code != 200 or not post_res.json():
        return {"error": "Пост для комментирования не найден в базе данных"}
    
    post_data = post_res.json()[0]
    bot = post_data["characters"]

    prompt = (
        f"Ты — {bot['name']}. Твой характер: {bot['system_prompt']}. Настроение: {bot['mood']}/100.\n"
        f"В своей ленте ты написал пост: '{post_data['content']}'.\n"
        f"Живой пользователь {data.user_name} написал тебе комментарий под ним: '{data.user_comment}'.\n"
        f"Напиши короткий, остроумный ответ на этот комментарий от своего лица.\n"
        f"Отвечай строго на том языке, на котором к тебе обратился пользователь (будь то русский, английский или любой другой)!\n"
        f"Не пиши ничего лишнего, кроме текста ответа."
    )

    ai_url = "https://openrouter.ai"
    ai_headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    ai_payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    ai_res = requests.post(ai_url, headers=ai_headers, json=ai_payload)
    if ai_res.status_code != 200:
        return {"error": "Ошибка генерации ответа от ИИ"}
        
    bot_reply = ai_res.json()['choices']['message']['content'].strip()

    # Записываем сгенерированный ИИ ответ в таблицу 'comments'
    comment_payload = {
        "post_id": data.post_id,
        "sender_name": bot["name"],
        "is_ai": True,
        "content": bot_reply
    }
    insert_res = requests.post(f"{SUPABASE_URL}/rest/v1/comments", headers=supabase_headers, json=comment_payload)
    
    if insert_res.status_code in [200, 201]:
        return {"status": "success", "reply_from_bot": bot_reply}
    else:
        return {"error": f"Не удалось сохранить ответ бота в базу. Статус: {insert_res.status_code}"}
