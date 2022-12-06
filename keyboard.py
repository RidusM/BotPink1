from typing import Collection

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

button_planning = KeyboardButton('Планирование')
button_marketing = KeyboardButton('Рекламные продукты')

button_updates = KeyboardButton('Обновить данные')

button_price_projcost = KeyboardButton('Редактировать проекты/сотрудников')

button_set_cost = KeyboardButton('Указать цену по проекту')
button_staff_cost = KeyboardButton('Указать ставку по сотруднику')

button_get_othect = KeyboardButton('Получить отчет')

button_now = KeyboardButton('Текущая неделя')
button_future = KeyboardButton('Следующая неделя')
button_back = KeyboardButton('Назад')

replykb=ReplyKeyboardMarkup(resize_keyboard=True).add(button_planning, button_marketing)
replykb2=ReplyKeyboardMarkup(resize_keyboard=True).add(button_updates, button_price_projcost, button_get_othect, button_back)
replykb3=ReplyKeyboardMarkup(resize_keyboard=True).add(button_set_cost, button_staff_cost, button_back)
replykb4=ReplyKeyboardMarkup(resize_keyboard=True).add(button_now, button_future, button_back)

def genmarkup_for_projects(data):

    markup = InlineKeyboardMarkup()
    for i in data:
        markup.add(InlineKeyboardButton(i[1], callback_data=i[0]))
    return markup

def genmarkup_for_staff(data):
    markup = InlineKeyboardMarkup()
    for i in data:
        markup.add(InlineKeyboardButton(i[1], callback_data=i[0]))
    return markup