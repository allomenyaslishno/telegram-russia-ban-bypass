# AI Wrapper Telegram Bot (aiogram 3.x)

Отдельный мини-проект бота-агрегатора нейросетей на `aiogram 3.x`.

## Что внутри
- интерфейс как в примере: reply-меню + inline выбор моделей;
- профиль с лимитами (демо);
- хранение состояния пользователя в памяти (`model/history/premium`);
- роутинг по выбранной модели;
- OpenAI-коннектор для GPT/o4 через `OPENAI_API_KEY`.

## Запуск

```bash
cd ai-wrapper-bot
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export BOT_TOKEN="<telegram_bot_token>"
export OPENAI_API_KEY="<openai_api_key>"  # опционально
python main.py
```

## Важно
Сейчас `users_db` — in-memory словарь (сброс при рестарте). Для продакшена вынести в SQLite/PostgreSQL.

## Расширение backend
В `main.py` в `MODEL_ROUTER` уже подготовлены точки для подключения:
- DeepSeek V3 / R1
- DALL-E 3
- FLUX.1 Kontext
