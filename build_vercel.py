import os

# Создаем папки
os.makedirs('tarot-app/api', exist_ok=True)

# 1. requirements.txt (Библиотеки для Vercel)
with open('tarot-app/requirements.txt', 'w', encoding='utf-8') as f:
    f.write("""fastapi==0.104.1
uvicorn==0.24.0
supabase==2.3.4
httpx==0.25.1
pydantic==2.5.2
""")

# 2. vercel.json (Настройки деплоя)
with open('tarot-app/vercel.json', 'w', encoding='utf-8') as f:
    f.write("""{
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    },
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/index.py"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}""")

# 3. api/index.py (Серверный бэкенд FastAPI)
backend_code = """from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from supabase import create_client, Client
import httpx
import hmac
import hashlib
import base64
import os
from urllib.parse import parse_qsl

app = FastAPI()

# Ключи будут браться из Environment Variables в Vercel
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY", "")
VK_SECRET_KEY = os.environ.get("VK_SECRET_KEY", "")

# Подключаем БД
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None

class DrawRequest(BaseModel):
    vk_sign: str
    vk_id: int
    card_index: int
    question: str = ""

def verify_vk_sign(url_params: str, secret: str) -> bool:
    # Заглушка проверки подписи ВК
    # В реальности тут код проверки HMAC-SHA256
    return True

@app.post("/api/draw")
async def draw_card(req: DrawRequest):
    if not verify_vk_sign(req.vk_sign, VK_SECRET_KEY):
        raise HTTPException(status_code=403, detail="Invalid VK Sign")
        
    ai_response = ""
    # Если юзер задал вопрос - идем в OpenRouter
    if req.question and OPENROUTER_KEY:
        async with httpx.AsyncClient() as client:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "HTTP-Referer": "https://tarot-vk.vercel.app"
            }
            payload = {
                "model": "mistralai/mistral-7b-instruct:free", # Бесплатная быстрая модель для тестов
                "messages": [
                    {"role": "system", "content": "Ты мистическая гадалка Таро. Отвечай коротко (1-2 предложения), таинственно и мудро на основе вытянутой карты."},
                    {"role": "user", "content": f"Я вытянул карту. Мой вопрос: {req.question}. Что скажешь?"}
                ]
            }
            resp = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                ai_response = data['choices'][0]['message']['content']

    # Тут будет логика записи в Supabase (Списание энергии, добавление пыли)
    
    return {
        "status": "success",
        "ai_text": ai_response,
        "energy_left": 0
    }
"""
with open('tarot-app/api/index.py', 'w', encoding='utf-8') as f:
    f.write(backend_code)

# 4. Обновляем HTML и переносим в папку tarot-app
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Добавляем CSS для вопроса
css_addition = """
        /* --- ВОПРОС НЕЙРОСЕТИ --- */
        .question-box { width: 100%; max-width: 260px; margin: 0 auto 15px auto; }
        .question-input { width: 100%; background: rgba(23, 10, 36, 0.6); border: 1px solid rgba(212, 175, 55, 0.4); color: var(--gold-light); padding: 12px 15px; border-radius: 20px; font-family: 'Cormorant Garamond', serif; font-size: 15px; outline: none; box-sizing: border-box; text-align: center; transition: 0.3s;}
        .question-input:focus { border-color: var(--gold); box-shadow: 0 0 10px rgba(212, 175, 55, 0.3); background: rgba(26, 15, 36, 0.8); }
        .question-input::placeholder { color: #8874a3; font-style: italic; }
        .ai-text { font-size: 14px; color: #f9f1b4; margin-top: 12px; font-style: italic; border-top: 1px dashed rgba(212, 175, 55, 0.3); padding-top: 12px; display: none; line-height: 1.4;}
"""
html = html.replace("/* --- ЭКРАНЫ --- */", css_addition + "\n        /* --- ЭКРАНЫ --- */")

# Добавляем поле ввода
html_addition = """
        <div class="question-box">
            <input type="text" id="userQuestion" class="question-input" placeholder="Спроси Вселенную (необязательно)..." autocomplete="off">
        </div>
        <div class="flip-card" id="card" onclick="flipCard()">
"""
html = html.replace('<div class="flip-card" id="card" onclick="flipCard()">', html_addition)

# Добавляем текстовый блок для нейросети
ai_div = """<div class="card-desc" id="cardDesc">Текст</div>
                    <div class="ai-text" id="aiResponse">Духи шепчут...</div>"""
html = html.replace('<div class="card-desc" id="cardDesc">Текст</div>', ai_div)

# Обновляем JS логику для имитации нейросети
js_addition = """
            const question = document.getElementById('userQuestion').value;
            if(question.trim() !== '') {
                document.getElementById('aiResponse').style.display = 'block';
                document.getElementById('aiResponse').innerText = "✨ Духи читают твой вопрос...";
                // Имитация ответа нейросети (пока не подключен реальный сервер)
                setTimeout(() => {
                    document.getElementById('aiResponse').innerText = "Ответ карт: Твой путь будет светлым, но потребует смелости. Действуй!";
                }, 2000);
            } else {
                document.getElementById('aiResponse').style.display = 'none';
            }
            
            document.getElementById('card').classList.add('flipped');
"""
html = html.replace("document.getElementById('card').classList.add('flipped');", js_addition)

with open('tarot-app/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Архитектура Serverless успешно создана!")