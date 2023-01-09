# This is a sample Python script.
import glob
import os.path
import random

from telebot import TeleBot, types

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# В google colab добавить: !pip install pyTelegramBotAPI
# Чтобы добавить новое слово — нужно его прописать в массиве DEFINITOINS на 12 строчке
# Важно все новые аббривиатуры в коде писать только с маленьких букв
# Пользователь в телеграм может писать и с большой и с маленькой — код всегда приводит к строчным

folder_dir = 'recipe'


# Загружаем слова поддержки
f = open('./data/thinks.txt', 'r', encoding='UTF-8')
thinks = f.read().split('\n')
f.close()

bot = TeleBot(token='5748253811:AAEF5ZqSHDHLkl-1Z-pxJ5_1Uo4T0jt4oeM', parse_mode='html')  # создание бота


# Команда start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Хочу рецепт")
    item2 = types.KeyboardButton("Нет сил готовить...")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(m.chat.id,
                     'Привет! Я помогу тебе выбрать, что приготовить на ужин. Ты много тестировал, заводил баг-репорты,'
                     ' создавал чек-листы и очень устал... Чтобы не тратить силы еще и на выбор блюда, которое нужно'
                     ' приготовить на ужин, я сделаю это за тебя! Нажми: \nХочу рецепт — для получения интересного'
                     ' рецепта\nНет сил готовить... — для получения моральной поддержки ',
                     reply_markup=markup)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # Если юзер прислал 1, выдаем ему рецепт
    if message.text.strip() == 'Хочу рецепт':
        # Читаем список всех txt файлов с рецептами
        recipes_files = glob.glob('./recipe/*.txt')
        # Выбираем рандомный рецепт из списка
        current_recipe_file = random.choice(recipes_files)
        # в названии пути файла заменяем все \\ на /
        current_recipe_file = current_recipe_file.replace("\\", '/')
        # из пути к файлу выбираем только его имя с расширением
        current_recipe_file = current_recipe_file.split('/')[-1]
        # пытаемся прочитать рядом лежащий файл с фото
        # для этого берем оригинальное название файла с рецептом без разрешения
        image_name = current_recipe_file.split('.')[-2]
        # генерируем полный путь до возможного файла с фото
        current_recipe_image_name = './recipe/'+image_name+'.jpg'
        # проверяем его наличие на диске
        if os.path.exists(current_recipe_image_name):
            # читаем файл
            img = open(current_recipe_image_name, 'rb')
            # отправляем файл
            bot.send_photo(message.chat.id, img)
        with open('./recipe/' + current_recipe_file, 'r', encoding='utf-8') as file:
            answer = file.read()
    # Если юзер прислал 2, выдаем фразу о доставке
    elif message.text.strip() == 'Нет сил готовить...':
        answer = random.choice(thinks)
        img = open('1.jpg', 'rb')
        bot.send_photo(message.chat.id, img)
    else:
        answer = 'Ой... кажется, я еще не умею читать сообщения с клавиатуры😥 Если хочешь написать мне, ' \
                 'жми по кнопкам моего меню.'
    # Отсылаем юзеру сообщение в его чат
    bot.send_message(message.chat.id, answer)


# Запускаем бота
bot.polling(none_stop=True, interval=0)