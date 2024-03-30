import telebot
from telebot import types
import os
from datetime import datetime

with open("../token.txt", 'r') as file:
    content = file.readline()
    bot = telebot.TeleBot(content)
    # bot = telebot.TeleBot('6717914204:AAHJ2lYo-eB5HQSdXRo_BWhxIRNi2w5nMjc')


# Функция для создания основной клавиатуры с двумя кнопками
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Загрузить фото')
    btn2 = types.KeyboardButton('Подробнее')
    markup.add(btn1, btn2)
    return markup


# Функция для создания клавиатуры с кнопками после загрузки фото
def post_photo_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('На кого')
    btn3 = types.KeyboardButton('%')
    markup.add(btn1, btn2, btn3)
    return markup


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=main_keyboard())


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == 'Загрузить фото':
        msg = bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото.')
        bot.register_next_step_handler(msg, process_photo_step)
    elif message.text == 'Подробнее':
        bot.send_message(message.chat.id, 'Здесь могут быть подробности о вашем боте или сервисе.')
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=main_keyboard())
    elif message.text == '%':
        msg = bot.send_message(message.chat.id, 'Введите имя:')
        bot.register_next_step_handler(msg, process_name_step)
    elif message.text == 'На кого':
        # Здесь может быть логика для обработки запроса "На кого"
        pass


# Обработчик загрузки фото
def process_photo_step(message):
    if message.content_type == 'photo':
        bot.reply_to(message, 'Фото загружено успешно!')

        bot.send_message(message.chat.id, 'Выберите следующее действие:', reply_markup=post_photo_keyboard())
    else:
        bot.send_message(message.chat.id, 'Это не фото. Пожалуйста, попробуйте ещё раз.', reply_markup=main_keyboard())

        # Функция для создания папки, если она еще не существует


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Папка '{folder_path}' успешно создана.")
    else:
        print(f"Папка '{folder_path}' уже существует.")

    # Функция для обработки шага загрузки фото


def process_photo_step(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Задаем путь для новой папки
        folder_path = '/'
        create_folder(folder_path)  # Создаем папку, если она не существует

        # Создаем уникальное имя для файла с помощью временной метки
        filename = os.path.join(folder_path, f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        with open(filename, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, 'Фото сохранено в указанной папке.')
    except Exception as e:
        bot.reply_to(message, f'Произошла ошибка: {e}')


# Обработчик ввода имени
def process_name_step(message):
    name = message.text
    bot.send_message(message.chat.id, f'Вы ввели имя: {name}')
    # Здесь может быть логика для обработки имени
    # Добавляем кнопку "Ответ"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Ответ')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Нажмите на кнопку "Ответ", чтобы продолжить.', reply_markup=markup)


# Запуск бота
bot.polling(none_stop=True)
