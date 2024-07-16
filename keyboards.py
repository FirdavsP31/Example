from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


car_menu = InlineKeyboardMarkup()
car_menu.add(InlineKeyboardButton(text='SellCar',callback_data='sellcar'))
car_menu.add(InlineKeyboardButton(text='BuyCar',callback_data='buycar'))