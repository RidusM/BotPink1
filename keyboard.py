from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_planning = KeyboardButton('Планирование')
button_marketing = KeyboardButton('Рекламные продукты')

button_updates = KeyboardButton('Обновить данные')

button_edit = KeyboardButton('Редактировать проекты/сотрудников')

button_set_cost = KeyboardButton('Указать цену по проекту')
button_staff_cost = KeyboardButton('Указать ставку по сотруднику')

button_get_report = KeyboardButton('Получить отчет')

button_now = KeyboardButton('Текущая неделя')
button_future = KeyboardButton('Следующая неделя')
button_fullback = KeyboardButton('К начальному окну')
button_back = KeyboardButton('Назад')

reply_keyboard_start = ReplyKeyboardMarkup(resize_keyboard=True).add(button_planning, button_marketing)
reply_keyboard_planning = ReplyKeyboardMarkup(resize_keyboard=True).add(button_updates, button_edit,
                                                                        button_get_report, button_fullback)
reply_keyboard_set_params = ReplyKeyboardMarkup(resize_keyboard=True).add(button_set_cost, button_staff_cost,
                                                                          button_back, button_fullback)
reply_keyboard_get_report = ReplyKeyboardMarkup(resize_keyboard=True).add(button_now, button_future,
                                                                          button_back, button_fullback)


def gen_inline_projects(data):
    markup = InlineKeyboardMarkup()
    for i in data:
        markup.add(InlineKeyboardButton(i[1], callback_data=i[0]))
    return markup


def gen_inline_staff(data):
    markup = InlineKeyboardMarkup()
    for i in data:
        markup.add(InlineKeyboardButton(i[1], callback_data=i[0]))
    return markup
