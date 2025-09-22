# 🤖 Telegram Bot на базе Mistral AI

Простой Telegram-бот, который выступает в роли консультанта по здоровью и генерирует текстовые посты на тему регуляции гормонов с помощью **Mistral AI API**.
Использует `pyTelegramBotAPI`, `mistralai` и `python-dotenv`.
<details>
<summary>🖥Развернуть демонстрационный скриншот</summary>
<img width="1061" height="734" alt="image" src="https://github.com/user-attachments/assets/0396beb3-65c1-46e5-a354-f83f8ddc2920" />
</details>

---

## 📌 Основные возможности

- 🚀 Генерация текстовых постов на основе пользовательского запроса
- 🧠 Выбор стиля генерации поста (логичный, креативный, сбалансированный)
- 📱 Простое взаимодействие через Telegram
- 🧾 Поддержка эмодзи и структурированного текста в ответах от AI

---

## 🔧 Требования

Для запуска бота вам понадобится:

- Python 3.8+
- Установленные зависимости:
  - `pyTelegramBotAPI==4.27.0`
  - `python-dotenv==1.1.1`
  - `mistralai==1.9.2`
- Учетные данные:
  - Telegram Bot Token
  - Mistral AI API Key

---

+## 📦 Установка

1.  Клонируйте репозиторий:

    ```bash
    git clone https://github.com/ваше-имя/my_test_osteron_bot.git
    cd my_test_osteron_bot
    ```

2.  Создайте и активируйте виртуальное окружение:

    ```bash
    python3 -m venv venv
    source venv/bin/activate # Для Windows: venv\Scripts\activate
    ```

3.  Установите зависимости:

    ```bash
    pip install -r requirements.txt
    ```

4.  Создайте файл `.env` в корне проекта и добавьте свои ключи:

    ```env
    TELEGRAM_BOT_TOKEN="ВАШ_Telegram_Bot_Token"
    MISTRAL_API_KEY="ВАШ_Mistral_AI_API_Key"
    ```

---

## 🚀 Запуск бота

```bash
python3 bot.py
```

Бот начнет работу и будет ожидать команды от пользователя.

---

## 📱 Использование

1.  Отправьте команду `/start` для приветствия.
2.  Выберите стиль генерации поста с помощью кнопок.
3.  Введите тему поста и ожидайте генерацию ответа.

---

## 📁 Структура проекта

```
.
├── bot.py               # Основной код бота
├── .env                 # Файл с токенами
├── .gitignore           # Файлы и папки, исключённые из контроля версий
├── LICENSE              # Файл лицензии
├── README.md            # Этот файл
└── requirements.txt     # Список зависимостей
```

---

## ⚠️ Возможные ошибки и решения

**Ошибка: `AuthenticationError` от Mistral AI**
Проверьте правильность ввода `MISTRAL_API_KEY` в `.env` файле.

**Ошибка: `Unauthorized` от Telegram**
Проверьте правильность `TELEGRAM_BOT_TOKEN` в `.env` файле.

**Ошибка: `No module named '...some_module...'`**
Убедитесь, что вы активировали виртуальное окружение (`source venv/bin/activate`) и установили все зависимости командой `pip install -r requirements.txt`.

---

## 📝 Лицензия

MIT License — см. файл `LICENSE` для деталей.
