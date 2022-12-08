import datetime
import json
from typing import Collection
import datetime
import requests as requests
from aiogram import Bot, types, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import sqlite3

from aiogram.types import CallbackQuery, InlineKeyboardButton, callback_query

import database
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
                                                 "\bВыберите дальнейшее действие", reply_markup=keyboard.replykb)

@dp.message_handler(content_types=['text'], text='Рекламные продукты')
async def marketing(message: types.Message):
    await bot.send_message(message.from_user.id, 'К сожалению функционал этой кнопки еще не работает', reply_markup=keyboard.replykb)

@dp.message_handler(content_types=['text'], text='Планирование')
async def text_handler_for_update(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите действие:", reply_markup=keyboard.replykb2)

@dp.message_handler(content_types=['text'], text='Обновить данные')
async def text_handler_forupp(message: types.Message):
    reader.project_reader()
    reader.staff_reader()
    await bot.send_message(message.from_user.id, "Обновил данные")

@dp.message_handler(content_types=['text'], text='Редактировать проекты/сотрудников')
async def handler_for_update(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите, что хотите отредактировать?", reply_markup=keyboard.replykb3)

@dp.message_handler(content_types=['text'], text='Указать цену по проекту')
async def text_handler(message: types.Message):
    await UpdateProjects.choosing_id_of_project.set()
    cursor.execute("SELECT * FROM Projects")
    data = cursor.fetchall()
    await bot.send_message(message.from_user.id, "Выберите проект из списка:", reply_markup=keyboard.genmarkup_for_projects(data))

@dp.message_handler(content_types=['text'], text='Указать ставку по сотруднику')
async def text_handler2(message: types.Message):
    await UpdateOfPayment.choosing_id_of_employee.set()
    cursor.execute("SELECT * FROM staff")
    data = cursor.fetchall()
    await bot.send_message(message.from_user.id, "Выберите ставку для сотрудника", reply_markup=keyboard.genmarkup_for_staff(data))

@dp.message_handler(content_types=['text'], text='Назад')
async def back(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите дальнейшее действие", reply_markup=keyboard.replykb)

@dp.callback_query_handler(lambda call: True, state=UpdateOfPayment.choosing_id_of_employee)
async def staffcostcallback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(f'Введите новую ставку р/ч')
    async with state.proxy() as data:
        data["idofemployee"] = callback_query.data
    await UpdateOfPayment.choosing_cost_of_employee.set()
    await callback_query.answer()

@dp.message_handler(state=UpdateOfPayment.choosing_cost_of_employee)
async def stafcost_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["costofproject"] = message.text
    db.table_update_staff_cost(data["costofproject"], data["idofemployee"])
    await state.finish()
    await bot.send_message(message.from_user.id, "Возвращаю вас к начальному окну", reply_markup=keyboard.replykb2)

@dp.callback_query_handler(lambda call: True, state=UpdateProjects.choosing_id_of_project)
async def stoptopupcall(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await callback_query.message.edit_text(f'Введите значение цены')
    async with state.proxy() as data:
        data["idofproject"] = callback_query.data
    await UpdateProjects.choosing_cost_of_project.set()
    await callback_query.answer()

@dp.message_handler(state=UpdateProjects.choosing_cost_of_project)
async def st_update(message: types.Message, state:FSMContext):
    cost_of_project = message.from_user.id
    async with state.proxy() as data:
        data["costofproject"] = message.text
    db.table_update_projects_cost(data["costofproject"], data["idofproject"])
    await state.finish()
    await bot.send_message(message.from_user.id, "Возвращаю вас к начальному окну", reply_markup=keyboard.replykb2)

@dp.message_handler(content_types=['text'], text='Получить отчет')
async def text_handler_forupp(message: types.Message):
    reader.tasks_reader2()
    reader.task_reader3()
    await bot.send_message(message.from_user.id, "Выберите одно из двух действий:", reply_markup=keyboard.replykb4)

@dp.message_handler(content_types=['text'], text='Текущая неделя')
async def send_doc(message: types.Message):
    this_dat = datetime.datetime.now()
    this_week = this_dat.isocalendar()[1]
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
        {reader.tasks_reader2(this_week)}
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
    {reader.task_reader3(this_week)}
    </tbody></table>
    </body></html>''')

    Html_file = open('index.html', 'w', encoding='cp1251', errors='ignore')
    Html_file.write(html_str)
    Html_file.close()
    Html_file2 = open('index.html', 'rb')
    await bot.send_document(message.from_user.id, Html_file2)

@dp.message_handler(content_types=['text'], text='Следующая неделя')
async def send_doc_next_week(message: types.Message):
    this_dat = datetime.datetime.now()
    this_week = this_dat.isocalendar()[1]
    html_str = (f'''<!DOCTYPE html>
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
        {reader.tasks_reader2(this_week+1)}
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
    {reader.task_reader3(this_week+1)}
    </tbody></table>
    </body></html>''')

    Html_file = open('index.html', 'w', encoding='cp1251', errors='ignore')
    Html_file.write(html_str)
    Html_file.close()
    Html_file2 = open('index.html', 'rb')
    await bot.send_document(message.from_user.id, Html_file2)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)