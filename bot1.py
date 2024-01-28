import os
import datetime
import json
import requests
import traceback
import math
from aiogram import Bot, types, Dispatcher, executor


bot = Bot(token='6427944969:AAH73wDXboppx3E0Q5ZFT1Mj07Kzf62T1R4')
dp = Dispatcher(bot)

city_names = list()

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
  await message.reply("Привет! Есть команды:\n"
                      "/add <city>\n"
                      "/weather\n"
                      "/clear")

@dp.message_handler(commands=["weather"])
async def weather_command(message: types.Message):
    if len(city_names) == 0:
        await message.reply("Нет городов в списке, добавьте их с помощью команды \\add <city>")
        return

    try:
        for city_name in city_names:
            #city_name=message.json.text
            response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city_name}&appid=b6f3dea68ddea45d9f1b67c2b7c27f6d")
            data = response.json()
            with open('package.json', 'w') as file:
                json.dump(data, file)
            city = data["name"]
            cur_temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]

            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])

            # продолжительность дня
            length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

            await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            f"Погода в городе: {city}\nТемпература: {cur_temp}°C \n"
            f"Влажность: {humidity}%\nДавление: {math.ceil(pressure / 1.333)} мм.рт.ст\nВетер: {wind} м/с \n"
            f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
            f"Хорошего дня!\n")
    except Exception as ex:
        await message.reply(traceback.format_exc())
        await message.reply(data)

@dp.message_handler(commands=["add"])
async def add_command(message: types.Message):
    # Если не переданы никакие аргументы, то
    if message["text"].find(" ") == -1:
        await message.reply("Укажите город")
        return
    (command, city_name, ) = message["text"].split(" ", maxsplit=1)
    city_names.append(city_name)
    print(len(city_names))
    await message.reply(f"Добавлен город: {city_name}")

@dp.message_handler(commands=["clear"])
async def start_command(message: types.Message):
    city_names.clear()
    await message.reply("Cписок городов пуст")

if __name__ == "__main__":
  # С помощью метода executor.start_polling опрашиваем
    # Dispatcher: ожидаем команду /start
  executor.start_polling(dp)


