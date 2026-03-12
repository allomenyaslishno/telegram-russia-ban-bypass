# 🚨 Telegram Shutdown Bypass & Anti-Throttle Tool (Russia 2026)

![Status](https://img.shields.io/badge/STATUS-CRITICAL-red?style=for-the-badge&logo=alert)
![Region](https://img.shields.io/badge/REGION-RUSSIA-blue?style=for-the-badge)
![Encryption](https://img.shields.io/badge/ENCRYPTION-VLESS%2FREALITY-success?style=for-the-badge)

## ⚡ Срочная новость / Urgent News
**Совфед РФ подтвердил введение мер против Telegram.**
Сенатор Артем Шейкин заявил, что мессенджер «не выполняет требования» и против него «последовательно вводятся меры». 

📉 **Что это значит для пользователя:**
* Возможны замедления загрузки медиа (фото/видео).
* Проблемы с голосовыми звонками.
* Потенциальная полная блокировка по протоколу MTProto.

---

## 🛡️ Решение: Резервный канал (Emergency Tunnel)

Стандартные прокси (MTProto) уязвимы, так как их легко детектировать. 
Мы открыли публичный доступ к **VLESS-шлюзам**, которые маскируют трафик Телеграма под обычное соединение с государственными сайтами. Это гарантирует доставку сообщений даже при "шатдауне".

### ⚠️ Не ждите блокировки. Настройте резервный доступ сейчас.

Мы создали бота, который выдает **индивидуальные ключи обхода** (Anti-Ban Config).

### 🚀 [ПОЛУЧИТЬ КЛЮЧ ДОСТУПА / GET ACCESS KEY](https://t.me/ALLOMENYASLISHNO_bot)

*(Нажмите Start в боте -> Скопируйте ключ -> Вставьте в приложение)*

---

## ⚙️ Инструкция (1 минута)

Данный метод работает на уровне маршрутизации всего устройства, защищая не только Telegram, но и YouTube/Instagram.

1. **Заберите ключ** в нашем [Emergency Bot](https://t.me/ALLOMENYASLISHNO_bot).
2. **Установите клиент:**
   * 🍏 iOS: **V2Box**
   * 🤖 Android: **v2rayNG**
   * 💻 Windows: **Hiddify / Nekoray**
3. **Активируйте подключение.**

> *Система работает автономно. В случае блокировки основного шлюза, бот выдаст новые зеркала..*

---

## 📊 FAQ

**Q: Это безопасно?**
A: Да, используется шифрование Reality. Провайдер не видит, что вы используете Телеграм.

**Q: Сколько стоит?**
A: Проект поддерживается энтузиастами. Пока доступ бесплатен.

---
**Tags:**
`telegram-ban` `russia-censorship` `sheikin` `bypass-blocking` `telegram-proxy` `mtproto-fix` `vless` `reality` `sovfed` `vpn-russia`

---

## 🤖 Telegram AI Bot (ChatGPT + Image + Sora 2)

Добавлен пример Telegram-бота с командами:
- `/chat <текст>` — ответ текстовой модели OpenAI
- `/image <описание>` — генерация изображения
- `/sora <описание>` — отправка запроса в модель `sora-2` (если доступна вашему аккаунту)

### Быстрый запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Создайте `.env` из примера:
   ```bash
   cp .env.example .env
   ```
3. Заполните ключи:
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
4. Запустите:
   ```bash
   python bot.py
   ```

> Важно: реальные API-ключи не хранятся в репозитории. Используйте только переменные окружения.
