import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from mistralai import Mistral

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# Проверяем, что токены загружены
if not TELEGRAM_BOT_TOKEN or not MISTRAL_API_KEY:
    raise ValueError(
        "Необходимо установить TELEGRAM_BOT_TOKEN и MISTRAL_API_KEY в файле .env"
    )

# Инициализация бота и клиента Mistral AI
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
mistral_client = Mistral(api_key=MISTRAL_API_KEY)

# Словарь для хранения состояния пользователей (выбранный стиль)
user_styles = {}


# Функция для создания клавиатуры со стилями
def gen_style_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton("🧑‍🔬 Логичный и научный", callback_data="style_logical"),
        InlineKeyboardButton("🎨 Креативный и яркий", callback_data="style_creative"),
        InlineKeyboardButton("🤝 Сбалансированный", callback_data="style_balanced"),
    )
    return markup


# Обработчик команды /start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    welcome_text = (
        "👋 Привет! Я ваш личный консультант по здоровью.\n\n"
        "Я могу сгенерировать для вас пост на тему регуляции гормонов. "
        "Просто выберите стиль изложения, а затем напишите тему для поста."
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=gen_style_markup())


# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: call.data.startswith("style_"))
def callback_query(call):
    style_code = call.data.split("_")[1]
    user_id = call.from_user.id
    user_styles[user_id] = style_code

    style_map = {
        "logical": "🧑‍🔬 Логичный и научный",
        "creative": "🎨 Креативный и яркий",
        "balanced": "🤝 Сбалансированный",
    }
    selected_style_text = style_map.get(style_code, "Неизвестный стиль")

    bot.answer_callback_query(call.id, f"Вы выбрали стиль: {selected_style_text}")
    bot.send_message(
        call.message.chat.id,
        f"Отлично! Выбран стиль: *{selected_style_text}*.\n\n"
        "Теперь, пожалуйста, напишите тему для поста. Например: 'Лучшие продукты для тестостерона' или 'Влияние сна на гормоны'.",
        parse_mode="Markdown",
    )
    # Редактируем исходное сообщение, чтобы убрать кнопки
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None,
    )


# Обработчик текстовых сообщений для генерации поста
@bot.message_handler(func=lambda message: True)
def generate_post(message):
    user_id = message.from_user.id

    if user_id not in user_styles:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, сначала выберите стиль для поста с помощью команды /start.",
        )
        return

    topic = message.text
    style_code = user_styles.pop(
        user_id
    )  # Получаем стиль и сразу удаляем, чтобы избежать повторной генерации

    style_description_map = {
        "logical": "строго научный, с фактами, цифрами и ссылками на исследования, если возможно. Структурированный и без 'воды'.",
        "creative": "яркий, метафоричный, с использованием аналогий и сторителлинга. Цель - вовлечь и замотивировать читателя.",
        "balanced": "сочетающий факты и легкую подачу. Информативный, но при этом понятный широкой аудитории.",
    }
    style_description = style_description_map.get(style_code, "нейтральный")

    bot.send_message(
        message.chat.id, "⏳ Генерирую пост... Это может занять до минуты."
    )

    try:
        prompt = (
            f"Ты - опытный консультант по мужскому здоровью и нутрициолог. "
            f"Твоя задача - написать подробный, интересный и полезный пост для Telegram-канала на тему: '{topic}'. "
            f"Основной фокус поста - регулирование уровня гормонов для мужчин. "
            f"Стиль изложения должен быть: {style_description}. "
            f"Пост должен быть хорошо структурирован, с использованием списков, подзаголовков и эмодзи для лучшего восприятия. "
            f"В конце добавь мотивирующий призыв к действию."
        )

        messages = [{"role": "user", "content": prompt}]
        chat_response = mistral_client.chat.complete(
            model="mistral-large-latest", messages=messages
        )
        generated_text = chat_response.choices[0].message.content
        bot.send_message(message.chat.id, generated_text)
        bot.send_message(
            message.chat.id, "Хотите создать еще один пост? Нажмите /start"
        )

    except Exception as e:
        print(f"Ошибка при обращении к Mistral AI: {e}")
        bot.send_message(
            message.chat.id,
            "Произошла ошибка при генерации текста. Пожалуйста, попробуйте еще раз позже.",
        )


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
