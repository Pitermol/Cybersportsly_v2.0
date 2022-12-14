import json
import time
import os

import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from lxml import html, etree
import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from test import calculate

token = "5445591182:AAE2UAGgzuLFP5cFhtmd8iGZL2HDOBF1t_8"
HEROES = ['Abaddon', 'Alchemist', 'Ancient Apparition', 'Anti-Mage', 'Arc Warden', 'Axe', 'Bane', 'Batrider',
          'Beastmaster', 'Bloodseeker', 'Bounty Hunter', 'Brewmaster', 'Bristleback', 'Broodmother',
          'Centaur Warrunner', 'Chaos Knight', 'Chen', 'Clinkz', 'Clockwerk', 'Crystal Maiden', 'Dark Seer',
          'Dark Willow', 'Dawnbreaker', 'Dazzle', 'Death Prophet', 'Disruptor', 'Doom', 'Dragon Knight', 'Drow Ranger',
          'Earth Spirit', 'Earthshaker', 'Elder Titan', 'Ember Spirit', 'Enchantress', 'Enigma', 'Faceless Void',
          'Grimstroke', 'Gyrocopter', 'Hoodwink', 'Huskar', 'Invoker', 'Io', 'Jakiro', 'Juggernaut',
          'Keeper of the Light', 'Kunkka', 'Legion Commander', 'Leshrac', 'Lich', 'Lifestealer', 'Lina', 'Lion',
          'Lone Druid', 'Luna', 'Lycan', 'Magnus', 'Marci', 'Mars', 'Medusa', 'Meepo', 'Mirana', 'Monkey King', 'Morphling',
          'Naga Siren', 'Nature\'s Prophet', 'Necrophos', 'Night Stalker', 'Nyx Assassin', 'Ogre Magi', 'Omniknight',
          'Oracle', 'Outworld Destroyer', 'Pangolier', 'Phantom Assassin', 'Phantom Lancer', 'Phoenix', 'Primal Beast', 'Puck', 'Pudge',
          'Pugna', 'Queen of Pain', 'Razor', 'Riki', 'Rubick', 'Sand King', 'Shadow Demon', 'Shadow Fiend',
          'Shadow Shaman', 'Silencer', 'Skywrath Mage', 'Slardar', 'Slark', 'Snapfire', 'Sniper', 'Spectre',
          'Spirit Breaker', 'Storm Spirit', 'Sven', 'Techies', 'Templar Assassin', 'Terrorblade', 'Tidehunter',
          'Timbersaw', 'Tinker', 'Tiny', 'Treant Protector', 'Troll Warlord', 'Tusk', 'Underlord', 'Undying', 'Ursa',
          'Vengeful Spirit', 'Venomancer', 'Viper', 'Visage', 'Void Spirit', 'Warlock', 'Weaver', 'Windranger',
          'Winter Wyvern', 'Witch Doctor', 'Wraith King', 'Zeus'] # 123

bot = Bot(token=token)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Picks(StatesGroup):
    rad1 = State()
    rad2 = State()
    rad3 = State()
    rad4 = State()
    rad5 = State()
    dire1 = State()
    dire2 = State()
    dire3 = State()
    dire4 = State()
    dire5 = State()


@dp.message_handler(commands=["start", "menu"])
async def introduction(message: types.Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("/Go"))
    with open("data.json", "w", encoding="utf-8") as f:
        f.write("{\"processing\":{}}")
    f.close()
    await message.reply("????????????????????????. ?????????? ???????????????? ??????????????, ?????????????????????? ?????????????? \"/go\"", reply_markup=keyboard)


@dp.message_handler(commands=["cancel"])
async def go(message: types.Message):
    id = str(message.chat.id)
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    f.close()
    if id in data["processing"]:
        data["processing"][id] = []
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        f.close()
        await message.reply("????????????????")


@dp.message_handler(commands=["Go"])
async def go(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    h100 = HEROES[:100]
    h23 = HEROES[100:]
    for i in range(0, len(h100) - 1, 3):
        keyboard.row(InlineKeyboardButton(h100[i], callback_data=f"n{i}"), InlineKeyboardButton(h100[i + 1],
                                                                                                callback_data=f"n{i + 1}"),
                     InlineKeyboardButton(h100[i + 2], callback_data=f"n{i + 2}"))

    keyboard.row(InlineKeyboardButton(h100[-1], callback_data=f"n{99}"))
    msg = await message.reply("???????????????? ?????????? ?????????????? Radiant ?????? ?????????????? \"????????????\" ?????? ????????????",
                              reply_markup=keyboard)
    keyboard = InlineKeyboardMarkup()
    for i in range(0, len(h23) - 2, 3):
        keyboard.row(InlineKeyboardButton(h23[i], callback_data=f"n{HEROES.index(h23[i])}"), 
            InlineKeyboardButton(h23[i + 1], callback_data=f"n{HEROES.index(h23[i + 1])}"),
                     InlineKeyboardButton(h23[i + 2], callback_data=f"n{HEROES.index(h23[i + 2])}"))
    keyboard.row(InlineKeyboardButton(h23[-2], callback_data=f"n{HEROES.index(h23[-2])}"), 
        InlineKeyboardButton(h23[-1], callback_data=f"n{HEROES.index(h23[-1])}"))
    msg1 = await message.reply("-", reply_markup=keyboard)

    msg = msg.message_id
    msg1 = msg1.message_id
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    f.close()
    data["processing"][str(message.chat.id)] = [msg, msg1]
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
    f.close()


@dp.callback_query_handler()
async def process(query: types.CallbackQuery):
    hero = query.data[1:]
    print(hero, HEROES[int(hero)])
    h100 = HEROES[:100]
    h21 = HEROES[100:]

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    f.close()
    data["processing"][str(query.message.chat.id)].append(hero)
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f)
    f.close()

    for hero_ind in data["processing"][str(query.message.chat.id)][2:]:
        # print("number: " + str(hero_ind))
        if int(hero_ind) <= 99:
            h100.remove(HEROES[int(hero_ind)])
        else:
            h21.remove(HEROES[int(hero_ind)])

    keyboard = InlineKeyboardMarkup()
    for i in range(0, len(h100) - len(h100) % 3, 3):
        keyboard.row(InlineKeyboardButton(h100[i], callback_data=f"n{HEROES.index(h100[i])}"),
                     InlineKeyboardButton(h100[i + 1],
                                          callback_data=f"n{HEROES.index(h100[i + 1])}"),
                     InlineKeyboardButton(h100[i + 2], callback_data=f"n{HEROES.index(h100[i + 2])}"))

    for i in range(1, len(h100) % 3 + 1):
        keyboard.row(InlineKeyboardButton(h100[-i], callback_data=f"n{HEROES.index(h100[-i])}"))

    if len(h21) != 23:
        keyboard1 = InlineKeyboardMarkup()
        for i in range(0, len(h21) - len(h21) % 3, 3):
            keyboard1.row(InlineKeyboardButton(h21[i], callback_data=f"n{HEROES.index(h21[i])}"),
                          InlineKeyboardButton(h21[i + 1],
                                               callback_data=f"n{HEROES.index(h21[i + 1])}"),
                          InlineKeyboardButton(h21[i + 2], callback_data=f"n{HEROES.index(h21[i + 2])}"))

        for i in range(1, len(h21) % 3 + 1):
            keyboard1.row(InlineKeyboardButton(h21[-i], callback_data=f"n{HEROES.index(h21[-i])}"))
        try:
            await bot.edit_message_text(text="-", chat_id=query.message.chat.id,
                                    message_id=data["processing"][str(query.message.chat.id)][1],
                                    reply_markup=keyboard1)
        except:
            print("no need")

    cur_heroes_rad = []
    cur_heroes_rad_inds = []
    cur_heroes_dire = []
    cur_heroes_dire_inds = []
    if len(data["processing"][str(query.message.chat.id)][2:]) <= 5:
        for h in data["processing"][str(query.message.chat.id)][2:]:
            ind = int(h)
            cur_heroes_rad.append(HEROES[ind])
            cur_heroes_rad_inds.append(ind)
    else:
        for h in data["processing"][str(query.message.chat.id)][2:7]:
            ind = int(h)
            cur_heroes_rad.append(HEROES[ind])
            cur_heroes_rad_inds.append(ind)
        for h in data["processing"][str(query.message.chat.id)][7:]:
            ind = int(h)
            cur_heroes_dire.append(HEROES[ind])
            cur_heroes_dire_inds.append(ind)
    new_text = f'''
        ?????????????????? ??????????: \n\tRadiant: {", ".join(cur_heroes_rad)}\n\tDire: {", ".join(cur_heroes_dire)}
    '''
    if len(cur_heroes_rad) < 5:
        new_text += "\n???????????????? ?????????? ?????????????? Radiant ?????? ?????????????? \"????????????\" ?????? ????????????"
        await bot.edit_message_text(text=new_text,
                                    chat_id=query.message.chat.id,
                                    message_id=data["processing"][str(query.message.chat.id)][0],
                                    reply_markup=keyboard)
    elif len(cur_heroes_dire) < 5:
        new_text += "\n???????????????? ?????????? ?????????????? Dire ?????? ?????????????? \"????????????\" ?????? ????????????"
        await bot.edit_message_text(text=new_text,
                                    chat_id=query.message.chat.id,
                                    message_id=data["processing"][str(query.message.chat.id)][0],
                                    reply_markup=keyboard)
    else:
        new_text += "\n????????????, ???????????? ??????????????, ???????????????????? ?????????????????????????????? ?????????? ?????????? ???????????????? ?????????? ????????????"
        await bot.edit_message_text(text=new_text,
                                    chat_id=query.message.chat.id,
                                    message_id=data["processing"][str(query.message.chat.id)][0])
        await bot.edit_message_text(text="+",
                                    chat_id=query.message.chat.id,
                                    message_id=data["processing"][str(query.message.chat.id)][1])

        points = calculate(cur_heroes_rad, cur_heroes_dire)

        print(points)
        time.sleep(2)

        if points <= -2.0:
            text = f"???????????? ??????????????. ??????????????:\n\t ?????????????????? ???????????? ?????????????? Dire"
        elif -2.0 < points < 0:
            text = f"???????????? ??????????????. ??????????????:\n\t ?????????????????????? ???????????? ?????????????? Dire"
        elif 0 < points < 2:
            text = f"???????????? ??????????????. ??????????????:\n\t ?????????????????????? ???????????? ?????????????? Radiant"
        elif points == 0:
            text = "?????????????? ?????????????????? ??????????"
        else:
            text = f"???????????? ??????????????. ??????????????:\n\t ?????????????????? ???????????? ?????????????? Radiant"

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton("/Go"))
        await bot.send_photo(query.message.chat.id, open("screen.png", "rb"))
        await bot.send_message(query.message.chat.id, text, reply_markup=keyboard)

        with open("data.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        f.close()
        data["processing"][str(query.message.chat.id)] = []
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
        f.close()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

# ?????????????? ???? ?????????????? ?????????????? ?????? ????????????, ???????????????? ???????????? ?????????? ???? ????????????
