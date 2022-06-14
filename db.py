from models import *
import csv


def create_db():
    db.init('food_map.db')
    db.connect()
    db.drop_tables([User])
    db.create_tables([User])
    cashtan = User(
        username='cashtan54',
        user_tg_id=408871919
    )
    cashtan.save()
    db.close()


def fill_food_table():
    db.init('food_map.db')
    db.connect()
    db.drop_tables([Food])
    db.create_tables([Food])
    with open('food.csv', 'r', encoding='utf-8', newline='') as file:
        data = csv.reader(file, dialect='excel')
        for food, description in data:
            if 'Нельзя' in description:
                allowed = False
            else:
                allowed = True
            food_inst = Food(
                name=food,
                is_allowed=allowed,
                description=description,
            )
            food_inst.save()
    db.close()


if __name__ == '__main__':
    create_db()
    fill_food_table()