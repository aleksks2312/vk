import re

with open('tarot-app/api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_code = """                        text = data['choices'][0]['message']['content']
                        text = text.replace('*', '').strip() # Чистим от возможных звездочек"""

new_code = """                        text = data['choices'][0]['message']['content']
                        # Вырезаем блоки <think>...</think> (встречаются у рассуждающих ИИ)
                        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
                        text = text.replace('<think>', '').replace('</think>', '')
                        text = text.replace('*', '').strip() # Чистим от возможных звездочек"""

code = code.replace(old_code, new_code)

with open('tarot-app/api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Backend patched for <think> tags!")