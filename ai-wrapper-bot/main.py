import asyncio
import logging
import os
from collections.abc import Awaitable, Callable

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)

from openai import AsyncOpenAI

TOKEN = os.getenv("BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not TOKEN:
    raise RuntimeError("Set BOT_TOKEN environment variable before running the bot.")

bot = Bot(token=TOKEN)
dp = Dispatcher()

users_db: dict[int, dict[str, object]] = {}

MODEL_LABELS: dict[str, str] = {
    "model_gpt5_nano": "GPT-5 nano",
    "model_gpt5_mini": "GPT-5 mini",
    "model_gpt5_premium": "GPT-5",
    "model_o4_mini": "o4-mini",
    "model_ds_v3": "DeepSeek V3",
    "model_ds_r1": "DeepSeek R1",
    "model_dalle3": "DALL-E 3",
    "model_flux_pro": "FLUX.1 Kontext [pro]",
}

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✏️ Текст"),
            KeyboardButton(text="🖼 Изображение"),
            KeyboardButton(text="🎙 Озвучка"),
        ],
        [
            KeyboardButton(text="🤖 Выбрать нейросеть"),
            KeyboardButton(text="👤 Профиль"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите действие...",
)


def get_models_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ GPT-5 nano", callback_data="model_gpt5_nano"),
                InlineKeyboardButton(text="GPT-5 mini", callback_data="model_gpt5_mini"),
            ],
            [
                InlineKeyboardButton(text="GPT-5 ⭐", callback_data="model_gpt5_premium"),
                InlineKeyboardButton(text="o4-mini ⭐💡", callback_data="model_o4_mini"),
            ],
            [
                InlineKeyboardButton(text="DeepSeek V3", callback_data="model_ds_v3"),
                InlineKeyboardButton(text="DeepSeek R1 ⭐💡", callback_data="model_ds_r1"),
            ],
            [
                InlineKeyboardButton(text="✅ DALL-E 3 🖼 ⭐", callback_data="model_dalle3"),
            ],
            [
                InlineKeyboardButton(
                    text="FLUX.1 Kontext [pro] 🖼 ⭐", callback_data="model_flux_pro"
                ),
            ],
            [InlineKeyboardButton(text="🗑 Очистить чат", callback_data="clear_context")],
        ]
    )


profile_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🌍 Сменить язык", callback_data="change_lang")],
        [InlineKeyboardButton(text="🌟 Купить Premium", callback_data="buy_premium")],
    ]
)


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    user_id = message.from_user.id
    users_db.setdefault(
        user_id,
        {
            "model": "model_gpt5_nano",
            "requests": 0,
            "history": [],
            "premium": False,
        },
    )

    await message.answer(
        "👋 Здравствуйте! Выберите необходимое действие, используя кнопки ниже.",
        reply_markup=main_menu,
    )


@dp.message(F.text == "🤖 Выбрать нейросеть")
async def show_models(message: Message) -> None:
    await message.answer(
        "<b>✏️ Выбор нейросети</b>\n"
        "Выберите нейросеть, чтобы начать ей пользоваться\n\n"
        "⭐ — Premium модели\n"
        "💡 — Рассуждающие модели\n"
        "🖼 — Модели для генерации изображений",
        reply_markup=get_models_keyboard(),
        parse_mode="HTML",
    )


@dp.message(F.text == "👤 Профиль")
async def show_profile(message: Message) -> None:
    user_id = message.from_user.id
    user = users_db.setdefault(user_id, {"model": "model_gpt5_nano", "requests": 0})

    limits_text = "- GPT-5 nano — 30/30\n- GPT-5 mini — 20/20\n- DeepSeek V3 — 10/10"
    text = (
        "👤 <b>Ваш профиль</b>\n"
        f"🌟 Premium: {'активирован' if user.get('premium') else 'не активирован'}.\n"
        "🌍 Текущий язык: Русский.\n"
        f"🆔 ID: {user_id}\n\n"
        "📊 <b>Лимиты:</b>\n"
        f"{limits_text}\n\n"
        "Лимиты обновляются каждый день в 0:00 по Москве."
    )
    await message.answer(text, reply_markup=profile_kb, parse_mode="HTML")


@dp.callback_query(F.data.startswith("model_"))
async def process_model_selection(callback: CallbackQuery) -> None:
    user = users_db.setdefault(callback.from_user.id, {"model": "model_gpt5_nano", "requests": 0})
    model_code = callback.data
    user["model"] = model_code
    model_name = MODEL_LABELS.get(model_code, model_code)

    await callback.answer(f"Выбрана модель: {model_name}")
    await callback.message.answer(
        f"✅ Режим переключен на <b>{model_name}</b>. Напишите запрос.",
        parse_mode="HTML",
    )


@dp.callback_query(F.data == "clear_context")
async def clear_context(callback: CallbackQuery) -> None:
    user = users_db.setdefault(callback.from_user.id, {"history": []})
    user["history"] = []
    await callback.answer("Контекст чата очищен")
    await callback.message.answer("🧹 История диалога очищена.")


async def call_openai(messages: list[dict[str, str]], model: str) -> str:
    if not OPENAI_API_KEY:
        return "OPENAI_API_KEY не задан. Добавьте ключ, чтобы получать реальные ответы."
    client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    completion = await client.chat.completions.create(model=model, messages=messages)
    return completion.choices[0].message.content or "Пустой ответ от модели."


def build_model_router() -> dict[str, Callable[[list[dict[str, str]]], Awaitable[str]]]:
    return {
        "model_gpt5_nano": lambda messages: call_openai(messages, "gpt-5-nano"),
        "model_gpt5_mini": lambda messages: call_openai(messages, "gpt-5-mini"),
        "model_gpt5_premium": lambda messages: call_openai(messages, "gpt-5"),
        "model_o4_mini": lambda messages: call_openai(messages, "o4-mini"),
        "model_ds_v3": lambda _messages: asyncio.sleep(0, result="DeepSeek V3 коннектор пока не подключен."),
        "model_ds_r1": lambda _messages: asyncio.sleep(0, result="DeepSeek R1 коннектор пока не подключен."),
        "model_dalle3": lambda _messages: asyncio.sleep(0, result="Генерация изображений DALL-E 3 пока не подключена."),
        "model_flux_pro": lambda _messages: asyncio.sleep(0, result="FLUX.1 коннектор пока не подключен."),
    }


MODEL_ROUTER = build_model_router()


@dp.message()
async def handle_ai_request(message: Message) -> None:
    user_id = message.from_user.id
    user = users_db.setdefault(user_id, {"model": "model_gpt5_nano", "history": []})
    model_code = str(user.get("model", "model_gpt5_nano"))
    model_name = MODEL_LABELS.get(model_code, model_code)

    history: list[dict[str, str]] = user.setdefault("history", [])
    history.append({"role": "user", "content": message.text or ""})

    model_handler = MODEL_ROUTER.get(model_code)
    if model_handler is None:
        response_text = f"Для модели {model_name} пока нет обработчика."
    else:
        response_text = await model_handler(history)

    history.append({"role": "assistant", "content": response_text})
    await message.answer(
        f"<b>{model_name}</b>\n\n{response_text}",
        parse_mode="HTML",
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
