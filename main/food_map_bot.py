import telebot
import csv

bot = telebot.TeleBot('5382174532:AAEuJdwo300DfHgwMQn-Y20_hq0AwMjC6ak')
google_search = 'https://www.google.com/search?q=Можно+ли+крысам+'


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
                     'Добро пожаловать!\nЭтот бот поможет Вам составить карту питания для Ваших крыс.')
    bot.send_message(m.chat.id, 'Для того, чтобы узнать, можно ли крысам тот или иной продукт, '
                                'просто введите его название. Например: Помидоры.\n'
                                'Если такого продукта в нашей базе нет, бот поищет ответ в интернете.')
    bot.send_message(m.chat.id, 'Для получения полного списка команд и возможностей бота нажмите /help')
    check_user(m.chat.id, m.from_user.username)


@bot.message_handler(content_types=['text'])
def find_food(m):
    with open(r'\RatsBot\data\food.csv', 'r', encoding='utf-8', newline='') as file:
        food_from_user = m.text.lower()
        data = csv.reader(file, dialect='excel')
        for food, description in data:
            if food_from_user in food:
                bot.send_message(m.chat.id, description)
                break
        else:
            search_in_google(m.chat.id, food_from_user)


def search_in_google(user, food_from_user):
    bot.send_message(user,
                     f'<a href="{google_search}{food_from_user}">{food_from_user}</a>',
                     parse_mode='HTML')


def check_user(id, username):
    with open(r'\RatsBot\data\users.txt', 'r+', encoding='utf-8') as file:
        users = file.readlines()
        if f'{id} {username}\n' not in users:
            file.write(f'{id} {username}\n')


bot.infinity_polling()