from aiogram import Bot,Dispatcher,types,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State,StatesGroup
from keyboards import car_menu
from datas import start_db,show_cars,add_to_db

class SellCar(StatesGroup):
    seller = State()
    model = State()
    horsepower = State()
    car_number = State()
    date = State()
    is_new = State()
    photo = State()
PROXY_URL = "http://proxy.server:3128/"
api = '7274736400:AAHbHH7P18acGnTjRQPS5HljGFit0HhgLnM'
bot = Bot(api,proxy=PROXY_URL)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

async def on_startup(_):
    await start_db()

@dp.message_handler(commands=['start'])
async def send_hi(xabar:types.Message):
    await xabar.answer(text='Hello!',reply_markup=car_menu)


@dp.callback_query_handler()
async def send_reg(call:types.CallbackQuery):
    data = call.data
    if data=='sellcar':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Здравствуйте\nНапишите свое имя для продажи машины!'
        )
        await SellCar.seller.set()
    elif data=='buycar':
        cars = await show_cars()
        for car in cars:
            await bot.send_photo(
                caption=f'''Отлично машина выставлена на продажу!,
name:{car[0]},
model:{car[1]},
horsepower:{car[2]},
nomer:{car[3]},
data:{car[4]},
new?:{car[5]},
photoCar:{car[6]},
 '''            )
@dp.message_handler(state=SellCar.seller)
async def send_model(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['name_user']=message.text
    await message.answer('напишите модель машины!')
    await SellCar.model.set()
@dp.message_handler(state=SellCar.model)
async def send_model(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['model']=message.text
    await message.answer('напишите сколько лошадильных сил в машине!')
    await SellCar.horsepower.set()
@dp.message_handler(state=SellCar.horsepower)
async def send_horse(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['horse_power']=message.text
    await message.answer('Теперь оставьте номер машины!')
    await SellCar.car_number.set()
@dp.message_handler(state=SellCar.car_number)
async def send_phone(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['num_car']=message.text
    await message.answer('Теперь оставьте дату машины!')
    await SellCar.date.set()
@dp.message_handler(state=SellCar.date)
async def send_email(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['birth_car']=message.text
    await message.answer('Теперь ответьте нам новый или бу машина!')
    await SellCar.is_new.set()
@dp.message_handler(state=SellCar.is_new)
async def send_birth(message:types.Message,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['new_car']=message.text
    await message.answer('Теперь отправьте нам фото машины для продажи!')
    await SellCar.photo.set()
@dp.message_handler(content_types='photo',state=SellCar.photo)
async def send_photo(photo:types.ContentType.PHOTO,state:FSMContext):
    async with state.proxy() as magliwmat:
        magliwmat['photoCar']=photo['photo'][0]['file_id']
    await bot.send_photo(caption=f'''Отлично машина выставлена на продажу!,
name:{magliwmat['name_user']},
model:{magliwmat['model']},
horsepower:{magliwmat['horse_power']},
nomer:{magliwmat['num_car']},
data:{magliwmat['birth_car']},
new?:{magliwmat['new_car']},
photoCar:{magliwmat['photoCar']},
 ''',
 
    photo=magliwmat['photoCar'],
    chat_id=photo.from_user.id)

    await  add_to_db(
        seller=magliwmat['name_user'],
        model=magliwmat['model'],
        horsepower=magliwmat['horse_power'],
        car_number=magliwmat['num_car'],
        date=magliwmat['birth_car'],
        is_new=magliwmat['new_car'],
        photo=magliwmat['photoCar']
    )
    await state.finish()
if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)