import sqlite3
from pathlib import Path
import random
import time
import telebot
from telebot import types
from api_sd import img2img
from delete_users_file import delete_file
from sql import minus_token, minus_gift_token, plus_token

bot = telebot.TeleBot('');

@bot.message_handler(commands=['start'])
def start(message):
    mes = message.chat.id
    img2 = open(f'static/img/13.png', 'rb')
    token = 3
    gift_token = 3
    id_user = message.chat.id
    name_users = message.from_user.username
    con = sqlite3.connect('db.db')
    cur = con.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int primary key, name varchar(50), token int, gift_token int)')
    con.commit()
    cur.execute("INSERT OR IGNORE INTO users (id, name, token, gift_token) VALUES ('%s','%s', '%s','%s')" % (id_user, name_users, token, gift_token))
    con.commit()
    cur.execute(f"SELECT gift_token FROM users WHERE id = {mes}")
    token_cortege = str(cur.fetchone())
    gift_token = int("".join(c for c in token_cortege if c.isalnum()))
    cur.close()
    con.close()

    #Создание кнопок меню
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('❤️‍🔥 Обработать фото', callback_data='undress', row_width=1)
    item2 = types.InlineKeyboardButton('💰 Пополнить', callback_data='money', row_width=2)
    item3 = types.InlineKeyboardButton('📝 Политика конфиденциальности', callback_data='police', row_width=2)
    item4 = types.InlineKeyboardButton('✉ Поддержка', callback_data='support', row_width=2)
    item5 = types.InlineKeyboardButton('👨 Личный кабинет', callback_data='LK', row_width=2)
    markup.add(item1, item2, item3, item4, item5)
    bot.send_photo(message.chat.id, img2, caption=f'Привет, {message.from_user.first_name}. Я - бот, который способен обработать фото по вашему запросу.'
                                                  '\n'
                                                  f'\n🎁 У тебя есть {gift_token} подарочных монетки! 🎁'
                                                  '\n'
                                                  f'\n🍥 1 монетка = 1 обработка. Для того, чтобы пополнить баланс, зайди в раздел меню "Пополнить" 🍥', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    mes = callback.message.chat.id
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT token FROM users WHERE id = {mes}")
    token_cortege = str(cur.fetchone())
    token = int("".join(c for c in token_cortege if c.isalnum()))
    cur.close()
    con.close()

    img1 = open(f'static/img/14.png', 'rb')
    if callback.data == 'undress':
        bot.send_photo(callback.message.chat.id, img1, caption="Для максимального результата придерживайся правил:\n\n🐟На фото должен быть один человек\n\nЖду фото😉")
    elif callback.data == 'support':
        bot.send_message(callback.message.chat.id,"Если у вас остались вопросы и предложение, то обращайтесь по этой электронной почте\nЕсли у вас возникла ошибка, обращайтесь по это эл. почте")
    elif callback.data == 'LK':
        bot.send_message(callback.message.chat.id, f"Пользователь: @{callback.message.chat.username}\nID: {mes}\n\nДоступно монет: {token}")

@bot.message_handler(content_types=['photo'])
def save_photo(message):
    # сохраним id чата в переменную
    mes = message.chat.id

    # создадим папку если её нет
    Path(f'files/{mes}/photos').mkdir(parents=True, exist_ok=True)

    #подключаем бд и вытаскиваем токены
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"SELECT token FROM users WHERE id = {mes}")
    token_cortege = str(cur.fetchone())
    token = int("".join(c for c in token_cortege if c.isalnum())) #значение токена
    cur.close()
    con.close()

    if not message.media_group_id:
        if token > 0:
            # Убираем один токен за обработку
            minus_token(mes)
            # убираем один подарочный токен за обработку
            minus_gift_token(mes)

            bot.send_message(message.chat.id, "⏳Обработка пошла...")

            time.sleep(3)

            bot.send_message(message.chat.id, f"Вы {random.randint(15,63)} в очереди!")

            # сохраним изображение
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = f'files/{mes}/' + file_info.file_path
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)

            try:
                img2img(mes, src)
                photo = open(f'files/{mes}/photos/photos_1.jpg', 'rb')
                bot.send_photo(message.chat.id, photo)
                photo.close()
            except :
                bot.send_message(message.chat.id, 'Извините, произошла техническая неполадка\nС вашего счета не спишется монетка, попробуйте позднее!')
                plus_token(mes)
            # Удалим ненежуные файлы
            delete_file(mes, src)

        else:
            bot.send_message(message.chat.id, "❗️❗️❗️У вас закончились монетки! Чтобы пополнить, зайдите в соответствующий раздел в главном меню")
    else:
        bot.send_message(message.chat.id, "Отправьте только одно фото за раз!")


@bot.message_handler(commands=['photo'])
def ass_ass(message):
    photo = open(f'files/{message.chat.id}/photos/file_113.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()
    photo = open(f'files/{message.chat.id}/photos/photos_1.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)
    photo.close()

bot.polling(none_stop=True)
