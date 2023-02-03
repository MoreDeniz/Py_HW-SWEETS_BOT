from create import dp
from aiogram import types
from aiogram.dispatcher.filters import Filter
from keyboard import kb_main_menu
from random import randint as RI
from datetime import datetime


@dp.message_handler(commands=['start'])
async def mes_start(message: types.Message):
    await message.answer(f'Привет тебе, {message.from_user.first_name}! Будем играть в конфетки 🍬🍬🍬)'
                         f'Нажми "/help", чтобы посмотреть правила или "/go" чтобы начать)',
                         reply_markup=kb_main_menu)
    user = []
    user.append(datetime.now())
    user.append(message.from_user.full_name)
    user.append(message.from_user.id)
    user.append(message.from_user.username)
    user.append(message.text)
    user = list(map(str, user))
    with open('spy.txt', 'a', encoding='UTF-8') as data:
        data.write(' | '.join(user) + '\n')

# Правила, кол-во конфет за 1 ход
@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    await message.answer(f'ПРАВИЛА ИГРЫ:\n Будем брать конфеты по очереди. Очередь определит жребий.'
                         f' За ход нужно взять от 1 до установленного количества конфет. '
                         f'Побеждает тот, кто берёт последнюю конфету.'
                         f'\n Нажми "/go", чтобы начать игру.')


@dp.message_handler(commands=['go'])
async def mes_settings(message: types.Message):
    global total
    global limit
    count = RI(100, 200)
    # count = int(message.text.split()[1])
    total = count
    set_limit = RI(15, 28)
    limit = set_limit
    await message.answer(f'Всего у нас {total} 🍬 конфет. За 1 ход можно взять от 1 🍬 '
                         f' до {limit} 🍬 конфет.',
                         reply_markup=kb_main_menu)
    # Жеребьёвка:
    toss = RI(0, 1)
    if toss == 0:
        bot_sweets = total % (limit + 1)
        if bot_sweets == 0:
            bot_sweets = limit
        total -= bot_sweets
        await message.answer('Жребий определил: первым ходит Бот!')
        await message.answer(f'Бот берёт {bot_sweets} конфет.\n'
                             f'На столе осталось {total} конфет.\n'
                             f' Твой ход. Бери конфеты!')
    else:
        await message.answer('Жребий определил: первым ходишь ты! Бери конфеты!')
    await mes_sweets(message)

@dp.message_handler(text=['bla','бла','Бла'])
async def mes_bla(message: types.Message):
    await message.answer('Бла Бла Бла')

@dp.message_handler()
async def mes_sweets(message: types.Message):
    global total
    global limit

    if message.text.isdigit():
        take_sweets = int(message.text)
        if take_sweets < 1:
            await message.answer('Надо взять хотя бы 1 🍬 конфету!')
        elif take_sweets > limit:
            await message.answer(f'Не надо жадничать! Больше {limit} 🍬 конфет брать нельзя!')
        elif take_sweets > total:
            await message.answer(f'Нельзя взять больше 🍬, чем осталось!')
        else:
            total -= take_sweets
            await message.answer(f'На столе осталось {total} 🍬 конфет.\n')
            if total == 0:
                await message.answer(f'Поздравляю, {message.from_user.first_name}, твоя победа!!!😋\n'
                                     f'Жми /start для возврата в меню или /go для новой игры)')
                return
            await message.answer(f'Ход Бота: ')
            bot_sweets = total % (limit + 1)
            if bot_sweets == 0:
                bot_sweets = limit
            total -= bot_sweets
            await message.answer(f'Бот взял {bot_sweets} 🍬 конфет. Осталось: {total} 🍬')
            if total == 0:
                await message.answer(f'{message.from_user.first_name}, Бот победил!!!😋\n'
                                     f'Жми /start для возврата в меню или /go для новой игры)')
                return
            await message.answer(f'Теперь твой ход, {message.from_user.first_name}!')
    else:
        await message.answer(f'Введи число !', reply_markup=kb_main_menu)
# от 1 до {limit}