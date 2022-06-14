import telebot
from db import *

bot = telebot.TeleBot('token')
google_search = 'https://www.google.com/search?q=Можно+ли+крысам+'
admin_username = 'cashtan54'
admin_id = 408871919


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
                     'Добро пожаловать!\nЭтот бот поможет Вам составить карту питания для Ваших крыс.')
    bot.send_message(m.chat.id, 'Для того, чтобы узнать, можно ли крысам тот или иной продукт, '
                                'просто введите его название. Например: Помидоры.\n'
                                'Если такого продукта в нашей базе нет, бот поищет ответ в интернете.\n'
                                'Для получения полного списка команд нажмите /help')
    add_user(m.from_user.username, m.from_user.id)


@bot.message_handler(commands=['help'])
def help(m):
    text_for_admin = '/allowed - список всех разрешенных продуктов\n' \
                     '/not_allowed - список всех запрещенных продуктов\n' \
                     '/add_food - добавить еду в бд'
    text_for_user = '/allowed - список всех разрешенных продуктов\n' \
                    '/not_allowed - список всех запрещенных продуктов\n'
    if m.from_user.id == admin_id:
        bot.send_message(m.chat.id, text_for_admin)
    else:
        bot.send_message(m.chat.id, text_for_user)


@bot.message_handler(commands=['add_food'])
def admin_add_food(m):
    if m.from_user.id == admin_id:
        sent = bot.send_message(m.chat.id, 'Enter food name to add:\nname\nis_allowed 0 or 1\ndescription')
        bot.register_next_step_handler(sent, add_food)


@bot.message_handler(commands=['allowed'])
def allowed_food(m):
    _allowed_food = list()
    for food in Food.select().where(Food.is_allowed == True):
        _allowed_food.append(food.name)
    bot.send_message(m.chat.id, '\n'.join(_allowed_food))


@bot.message_handler(commands=['not_allowed'])
def not_allowed_food(m):
    _not_allowed_food = list()
    for food in Food.select().where(Food.is_allowed == False):
        _not_allowed_food.append(food.name)
    bot.send_message(m.chat.id, '\n'.join(_not_allowed_food))


@bot.message_handler(content_types=['text'])
def find_food(m):
    food_from_user = m.text.lower()
    food_description = Food.get_or_none(Food.name.contains(food_from_user))
    if food_description:
        bot.send_message(m.chat.id, food_description.description)
    else:
        search_in_google(m.chat.id, food_from_user)


def add_food(m):
    food = m.text.split('\n')
    food_to_db = Food(
        name=food[0],
        is_allowed=(food[1] == '1'),
        description=food[2],
    )
    food_to_db.save()
    bot.send_message(admin_id, 'success')


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
