import telebot
import schedule
import time
import threading

# Токен твоего бота
TOKEN = '8169526052:AAEc5fFdqJoryoaN9UfQBQ8jRPQNaI4YUkc'
bot = telebot.TeleBot(TOKEN)

# ID чата, куда отправлять напоминания
CHAT_ID = None

# Тексты напоминаний
MORNING_REMINDER = "Доброе утро! 🌅 Не забудь о практике Чистой Близости. Сегодня — твой день быть собой."
EVENING_REMINDER = "Спокойного вечера 🌙 Подведи итоги дня, почувствуй благодарность и отпусти напряжение."

# Команда /start для активации напоминаний
@bot.message_handler(commands=['start'])
def send_welcome(message):
    global CHAT_ID
    CHAT_ID = message.chat.id
    bot.reply_to(message, "Привет! Я буду напоминать тебе о практике каждый день утром и вечером. Чтобы отключить напоминания, напиши /stop.")

# Команда /stop для отключения напоминаний
@bot.message_handler(commands=['stop'])
def stop_reminders(message):
    global CHAT_ID
    CHAT_ID = None
    bot.reply_to(message, "Напоминания отключены. Чтобы включить снова, напиши /start.")

# Напоминания по расписанию
def job_morning():
    if CHAT_ID:
        bot.send_message(CHAT_ID, MORNING_REMINDER)

def job_evening():
    if CHAT_ID:
        bot.send_message(CHAT_ID, EVENING_REMINDER)

# Планировщик задач
def schedule_jobs():
    schedule.every().day.at("09:00").do(job_morning)
    schedule.every().day.at("21:00").do(job_evening)

    while True:
        schedule.run_pending()
        time.sleep(30)

# Запуск планировщика в отдельном потоке
threading.Thread(target=schedule_jobs, daemon=True).start()

# Запуск бота
bot.infinity_polling()
