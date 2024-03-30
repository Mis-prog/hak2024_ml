import telebot
from telebot import types
import os
from datetime import datetime


def init_bot():
    with open("token.txt", 'r') as file:
        content = file.readline()
        bot = telebot.TeleBot(content)
    return bot


bot = init_bot()


# Функция для создания основной клавиатуры с двумя кнопками
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Загрузить фото')
    btn2 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2)
    return markup

def main_keyboard_two():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    btn2 = types.KeyboardButton('Помощь')
    markup.add(btn1, btn2)
    return markup


# Функция для создания клавиатуры с кнопками после загрузки фото
def post_photo_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Назад')
    markup.add(btn1)
    return markup

def send_developer_link(message):
    developer_link = 'https://example.com/developers'
    message_text = f'Ссылка на разработчиков: [{developer_link}]({developer_link})'
    bot.send_message(message.chat.id, message_text, parse_mode='Markdown')


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, 'Загрузить фото:', reply_markup=main_keyboard())


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == 'Загрузить фото':
        msg = bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото.',reply_markup=main_keyboard_two())

        bot.register_next_step_handler(msg, process_photo_step)
    elif message.text == 'Помощь':
        send_developer_link(message)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото:', reply_markup=main_keyboard())
    # elif message.text == '%':
    #     msg = bot.send_message(message.chat.id, 'Введите имя:')
    #     bot.register_next_step_handler(msg, process_name_step)
    # elif message.text == '':
        pass

def send_developer_link(message):
    developer_link = 'https://t.me/Ganya_Lo'
    message_text = f'Ссылка на разработчиков: [{developer_link}]({developer_link})'
    bot.send_message(message.chat.id, message_text, parse_mode='Markdown',reply_markup=main_keyboard())

# Обработчик загрузки фото
# def process_photo_step(message):
#
#     if (message.content_type != 'photo') and (message.text!="Назад"):
#         bot.send_message(message.chat.id, 'Фото загружено успешно!')
#
#         file_info = bot.get_file(message.photo[-1].file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
#         folder_path = '/photo'
#         create_folder(folder_path)
#         filename = os.path.join(folder_path, f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
#         with open(filename, 'wb') as new_file:
#             new_file.write(downloaded_file)
#
#         bot.send_message(message.chat.id, 'Выберите следующее действие:', reply_markup=post_photo_keyboard())
#     elif message.text=="Назад":
#         bot.send_message(message.chat.id,'Пожалуйста, загрузите ваше фото:', reply_markup=main_keyboard())
#     else:
#         bot.send_message(message.chat.id, 'Это не фото. Пожалуйста, попробуйте ещё раз.', reply_markup=main_keyboard())
#
#


def process_photo_step(message):
    if message.content_type == 'photo':
        try:
            # Получаем информацию о загруженном файле
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Создаем папку для сохранения фотографии
            folder_path = './photo'  # Путь к папке (относительный)
            create_folder(folder_path)  # Создаем папку, если она не существует

            # Создаем уникальное имя для файла
            filename = os.path.join(folder_path, f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")

            # Сохраняем фото в файл
            with open(filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Отправляем сообщение об успешном сохранении фотографии
            bot.send_message(message.chat.id, 'Фотография успешно сохранена.')

            # Отправляем пользователю клавиатуру с дополнительными действиями
            bot.send_message(message.chat.id,"Выберите следующее дейсвие",reply_markup=main_keyboard())
        except Exception as e:
            # Обработка ошибки
            bot.send_message(message.chat.id, f'Произошла ошибка: {e}')
    elif message.text == 'Назад':
        # Если пользователь нажал кнопку "Назад"
        bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото:', reply_markup=main_keyboard())

    elif message.text == 'Помощь':
        send_developer_link(message)
    else:
        # Если загруженный контент не является фотографией
        bot.send_message(message.chat.id, 'Это не фотография. Пожалуйста, загрузите фотографию.',
                         reply_markup=main_keyboard())
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


#     # Функция для обработки шага загрузки фото
#
#
# def process_photo_step(message):
#     try:
#         file_info = bot.get_file(message.photo[-1].file_id)
#         downloaded_file = bot.download_file(file_info.file_path)
#
#         # Задаем путь для новой папки
#         folder_path = '/'
#         create_folder(folder_path)  # Создаем папку, если она не существует
#
#         # Создаем уникальное имя для файла с помощью временной метки
#         filename = os.path.join(folder_path, f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
#         with open(filename, 'wb') as new_file:
#             new_file.write(downloaded_file)
#         bot.reply_to(message, 'Фото сохранено в указанной папке.')
#     except Exception as e:
#         bot.reply_to(message, f'Произошла ошибка: {e}')


# # Обработчик ввода имени
# def process_name_step(message):
#     name = message.text
#     bot.send_message(message.chat.id, f'Вы ввели имя: {name}')
#     # Здесь может быть логика для обработки имени
#     # Добавляем кнопку "Ответ"
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#     btn1 = types.KeyboardButton('Ответ')
#     markup.add(btn1)
#     bot.send_message(message.chat.id, 'Нажмите на кнопку "Ответ", чтобы продолжить.', reply_markup=markup)


# Запуск бота
bot.polling(none_stop=True)
