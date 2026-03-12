import asyncio
import base64
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import BufferedInputFile, Message
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHAT_MODEL = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gpt-image-1")
SORA_MODEL = os.getenv("SORA_MODEL", "sora-2")

if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("Переменная TELEGRAM_BOT_TOKEN не задана")

if not OPENAI_API_KEY:
    raise RuntimeError("Переменная OPENAI_API_KEY не задана")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)


@dp.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет! Я бот с командами:\n"
        "/chat <текст> — ответ модели ChatGPT\n"
        "/image <описание> — генерация изображения\n"
        "/sora <описание> — создание видео-запроса для Sora 2"
    )


@dp.message(Command("chat"))
async def handle_chat(message: Message) -> None:
    prompt = message.text.removeprefix("/chat").strip() if message.text else ""
    if not prompt:
        await message.answer("Добавьте текст после команды: /chat Ваш вопрос")
        return

    response = await client.responses.create(
        model=CHAT_MODEL,
        input=prompt,
    )

    text = response.output_text or "Пустой ответ от модели."
    await message.answer(text)


@dp.message(Command("image"))
async def handle_image(message: Message) -> None:
    prompt = message.text.removeprefix("/image").strip() if message.text else ""
    if not prompt:
        await message.answer("Добавьте описание после команды: /image Неоновый город ночью")
        return

    result = await client.images.generate(
        model=IMAGE_MODEL,
        prompt=prompt,
        size="1024x1024",
    )

    image_b64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_b64)
    photo = BufferedInputFile(image_bytes, filename="generated.png")
    await message.answer_photo(photo=photo, caption="Готово")


@dp.message(Command("sora"))
async def handle_sora(message: Message) -> None:
    prompt = message.text.removeprefix("/sora").strip() if message.text else ""
    if not prompt:
        await message.answer("Добавьте описание после команды: /sora Кинематографичный полет дрона над горами")
        return

    try:
        # На момент написания доступ к Sora API ограничен.
        # Этот вызов показывает ожидаемую структуру запроса.
        job = await client.responses.create(
            model=SORA_MODEL,
            input=f"Create a video with this prompt: {prompt}",
        )
        await message.answer(
            "Запрос в Sora 2 отправлен.\n"
            f"Model: {SORA_MODEL}\n"
            f"Job info: {job.output_text or 'без текстового ответа'}"
        )
    except Exception as exc:
        await message.answer(
            "Sora 2 API может быть недоступен для вашего аккаунта.\n"
            f"Техническая ошибка: {exc}"
        )


@dp.message(F.text)
async def handle_default(message: Message) -> None:
    await message.answer("Используйте /chat, /image или /sora")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
