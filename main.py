import datetime
from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import sqlite3

import database as db
import reader

import keyboard
from config import Token


class UpdateProjects(StatesGroup):
    choosing_id_of_project = State()
    choosing_cost_of_project = State()


class UpdateOfPayment(StatesGroup):
    choosing_id_of_employee = State()
    choosing_cost_of_employee = State()


conn = sqlite3.connect('BotDataBase.db')
cursor = conn.cursor()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=Token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, "Привет, я бот Пинк для получения информаци"
                                                 "\bВыберите дальнейшее действие",
                           reply_markup=keyboard.reply_keyboard_start)


@dp.message_handler(content_types=['text'], text='Рекламные продукты')
async def marketing(message: types.Message):
    await bot.send_message(message.from_user.id, 'К сожалению функционал этой кнопки еще не работает',
                           reply_markup=keyboard.reply_keyboard_start)


@dp.message_handler(content_types=['text'], text='Планирование')
async def planning(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=keyboard.reply_keyboard_planning)


@dp.message_handler(content_types=['text'], text='Обновить данные')
async def update_info(message: types.Message):
    reader.get_list_project()
    reader.get_list_staff()
    await bot.send_message(message.from_user.id, "Обновил данные")


@dp.message_handler(content_types=['text'], text='Редактировать проекты/сотрудников')
async def choice_of_edit(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите, что хотите отредактировать?",
                           reply_markup=keyboard.reply_keyboard_set_params)


@dp.message_handler(content_types=['text'], text='Указать цену по проекту')
async def edit_cost_proj(message: types.Message):
    await UpdateProjects.choosing_id_of_project.set()
    cursor.execute("SELECT * FROM Projects")
    data = cursor.fetchall()
    await bot.send_message(message.from_user.id, "Выберите проект из списка:",
                           reply_markup=keyboard.gen_inline_for_projects(data))


@dp.message_handler(content_types=['text'], text='Указать ставку по сотруднику')
async def edit_cost_staff(message: types.Message):
    await UpdateOfPayment.choosing_id_of_employee.set()
    cursor.execute("SELECT * FROM staff")
    data = cursor.fetchall()
    await bot.send_message(message.from_user.id, "Выберите ставку для сотрудника",
                           reply_markup=keyboard.gen_inline_for_staff(data))


@dp.message_handler(content_types=['text'], text='К начальному окну')
async def fullback(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите дальнейшее действие",
                           reply_markup=keyboard.reply_keyboard_start)


@dp.message_handler(content_types=['text'], text='Назад')
async def back(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите дальнейшее действие",
                           reply_markup=keyboard.reply_keyboard_planning)


@dp.callback_query_handler(lambda call: True, state=UpdateOfPayment.choosing_id_of_employee)
async def staff_cost_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(f'Введите новую ставку р/ч')
    async with state.proxy() as data:
        data["idofemployee"] = callback_query.data
    await UpdateOfPayment.choosing_cost_of_employee.set()
    await callback_query.answer()


@dp.message_handler(state=UpdateOfPayment.choosing_cost_of_employee)
async def staff_cost_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["costofproject"] = message.text
    db.table_update_staff_cost(data["costofproject"], data["idofemployee"])
    await state.finish()
    await bot.send_message(message.from_user.id, "Выберте дальнейшее действие",
                           reply_markup=keyboard.reply_keyboard_set_params)


@dp.callback_query_handler(lambda call: True, state=UpdateProjects.choosing_id_of_project)
async def project_cost_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(f'Введите значение цены')
    async with state.proxy() as data:
        data["idofproject"] = callback_query.data
    await UpdateProjects.choosing_cost_of_project.set()
    await callback_query.answer()


@dp.message_handler(state=UpdateProjects.choosing_cost_of_project)
async def project_cost_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["costofproject"] = message.text
    db.table_update_projects_cost(data["costofproject"], data["idofproject"])
    await state.finish()
    await bot.send_message(message.from_user.id, "Выберите дальнейшее действие",
                           reply_markup=keyboard.reply_keyboard_set_params)


@dp.message_handler(content_types=['text'], text='Получить отчет')
async def text_handler_for_report(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите одно из двух действий:",
                           reply_markup=keyboard.reply_keyboard_get_report)


@dp.message_handler(content_types=['text'], text='Текущая неделя')
async def send_report_this_week(message: types.Message):
    await bot.send_message(message.from_user.id, "Идет загрузка отчета")
    this_dat = datetime.datetime.now()
    this_week = this_dat.isocalendar()[1]
    html_projects, html_staff = reader.tasks_reader2(this_week)
    html_str = (f'''<!DOCTYPE html>
        <html><head></head><body><h1>Распределение нагрузки на проектам</h1>
    <h2>Неделя {this_week}</h2>
    <table border="1">
        <tbody><tr>
            <td>#</td>
            <td>Проект</td>
            <td>Кол-во задач</td>
            <td>Плановая нагрузка, ч</td>
            <td>Плановая стоимость недели</td>
            <td>Себестоимость недели</td>
            <td>Доля загрузки проекта</td>
        </tr>
        {html_projects}
    </tbody></table>
    <h1>Распределение нагрузки на специалистов</h1>
<h2>Неделя {this_week}</h2>
<table border=1>
    <tr>
        <td>#</td>
        <td>Специалист</td>
        <td>Кол-во проектов</td>
        <td>Кол-во задач</td>
        <td>Плановая нагрузка, ч</td>
        <td>Себестоимость недели</td>
        <td>Плановая стоимость специалиста</td>
        <td>Доля нагрузки специалиста</td>
    </tr>
    {html_staff}
    </tbody></table>
    </body></html>''')

    html_file = open('index.html', 'w', encoding='cp1251', errors='ignore')
    html_file.write(html_str)
    html_file.close()
    html_file2 = open('index.html', 'rb')
    await bot.send_document(message.from_user.id, html_file2)


@dp.message_handler(content_types=['text'], text='Следующая неделя')
async def send_report_next_week(message: types.Message):
    await bot.send_message(message.from_user.id, "Идет загрузка отчета")
    this_dat = datetime.datetime.now()
    this_week = this_dat.isocalendar()[1]
    html_projects, html_staff = reader.tasks_reader2(this_week+1)
    html_str = (f'''
    <!DOCTYPE html>
    <html><head></head><body><h1>Распределение нагрузки на проектам</h1>
    <h2>Неделя {this_week+1}</h2>
    <table border="1">
        <tbody><tr>
            <td>#</td>
            <td>Проект</td>
            <td>Кол-во задач</td>
            <td>Плановая нагрузка, ч</td>
            <td>Плановая стоимость недели</td>
            <td>Себестоимость недели</td>
            <td>Доля загрузки проекта</td>
        </tr>
        {html_projects}
    </tbody></table>
    <h1>Распределение нагрузки на специалистов</h1>
<h2>Неделя {this_week+1}</h2>
<table border=1>
    <tr>
        <td>#</td>
        <td>Специалист</td>
        <td>Кол-во проектов</td>
        <td>Кол-во задач</td>
        <td>Плановая нагрузка, ч</td>
        <td>Себестоимость недели</td>
        <td>Плановая стоимость специалиста</td>
        <td>Доля нагрузки специалиста</td>
    </tr>
    {html_staff}
    </tbody></table>
    </body></html>''')

    html_file = open('index.html', 'w', encoding='cp1251', errors='ignore')
    html_file.write(html_str)
    html_file.close()
    html_file2 = open('index.html', 'rb')
    await bot.send_document(message.from_user.id, html_file2)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
