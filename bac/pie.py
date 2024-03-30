import telebot
from telebot import types
from datetime import datetime
from super_main import *


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


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, 'Загрузить фото:', reply_markup=main_keyboard())


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == 'Загрузить фото':
        msg = bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото.', reply_markup=main_keyboard_two())

        bot.register_next_step_handler(msg, process_photo_step)




    elif message.text == 'Помощь':
        send_developer_link(message)
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото:', reply_markup=main_keyboard())
        pass


def send_developer_link(message):
    developer_link = 'https://t.me/Ganya_Lo'
    message_text = f'Ссылка на разработчиков: [{developer_link}]({developer_link})'
    bot.send_message(message.chat.id, message_text, parse_mode='Markdown', reply_markup=main_keyboard())


def process_photo_step(message):
    global path_to_path;
    if message.content_type == 'photo':
        try:
            file_info = bot.get_file(message.photo[-1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            folder_path = '../photo'  # Путь к папке (относительный)
            create_folder(folder_path)  # Создаем папку, если она не существует

            path_to_photo = f"photo_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            filename = os.path.join(folder_path + '/', path_to_photo)

            with open(filename, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, 'Фотография успешно сохранена.')

            path_your_photo(filename)
            inform, image_path ,cos_val= method_name(filename)
            photo = method_name_(image_path)
            bot.send_photo(message.chat.id, photo)
            bot.send_message(message.chat.id,
                             f'"степень схожести : {round(cos_val*100,3)}%\n ',
                             reply_markup=main_keyboard())
            if "link" in inform:
                bot.send_message(message.chat.id,
                                 f'Основная информация о знаменитости \n Имя : {inform["name"].item()} ,\n Ссылка на кинопоиск : {inform["link"].item()} ,\n Фильмография : {inform["films_years"].item()}',
                                 reply_markup=main_keyboard())

            else:
                bot.send_message(message.chat.id,
                                 f'Основная информация о блогере \n Имя : {inform["name"].item()}',
                                 reply_markup=main_keyboard())

            bot.send_message(message.chat.id, "Выберите следующее дейсвие", reply_markup=main_keyboard())
        except Exception as e:
            bot.send_message(message.chat.id, f'Произошла ошибка: {e}')
    elif message.text == 'Назад':
        bot.send_message(message.chat.id, 'Пожалуйста, загрузите ваше фото:', reply_markup=main_keyboard())

    elif message.text == 'Помощь':
        send_developer_link(message)
    else:
        bot.send_message(message.chat.id, 'Это не фотография. Пожалуйста, загрузите фотографию.',
                         reply_markup=main_keyboard())


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


bot.polling(none_stop=True)
