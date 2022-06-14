import telebot
from db import *

bot = telebot.TeleBot('5382174532:AAEuJdwo300DfHgwMQn-Y20_hq0AwMjC6ak')
google_search = 'https://www.google.com/search?q=Можно+ли+крысам+'
admin_username = 'cashtan54'
admin_id = '408871919'


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
                     'Добро пожаловать!\nЭтот бот поможет Вам составить карту питания для Ваших крыс.')
    bot.send_message(m.chat.id, 'Для того, чтобы узнать, можно ли крысам тот или иной продукт, '
                                'просто введите его название. Например: Помидоры.\n'
                                'Если такого продукта в нашей базе нет, бот поищет ответ в интернете.')
    add_user(m.from_user.username, m.from_user.id)


@bot.message_handler(content_types=['text'])
def find_food(m):
    food_from_user = m.text.lower()
    food_description = Food.get_or_none(Food.name.contains(food_from_user))
    if food_description:
        bot.send_message(m.chat.id, food_description.description)
    else:
        search_in_google(m.chat.id, food_from_user)


@bot.message_handler(commands=['add_food'])
def add_food(m):
    if m.from_user.id == admin_id:
        bot.send_message(m.chat.id, 'Enter food name to add')


def search_in_google(user, food_from_user):
    bot.send_message(user,
                     f'<a href="{google_search}{food_from_user}">{food_from_user}</a>',
                     parse_mode='HTML')


def add_user(username, user_id):
    try:
        user = User(
            username=username,
            user_tg_id=user_id
        )
        user.save()
    except IntegrityError:
        pass


def _init_db():
    db.init('food_map.db')
    db.connect()


if __name__ == '__main__':
    _init_db()
    bot.infinity_polling()
    db.close()
