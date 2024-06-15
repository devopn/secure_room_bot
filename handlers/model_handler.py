import base64
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import httpx
router = Router()
from config import config
HOST = config.host

@router.callback_query(F.data.startswith("model"))
async def model_handler(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Введите желаемое имя", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Отмена")]],resize_keyboard=True))
    await state.set_state("model_name")

@router.message(StateFilter("model_name"))
async def model_handler(message: types.Message, state: FSMContext):
    name = message.text
    await state.set_data({"name": name})
    if name == "Отмена":
        await message.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer("Отлично, а теперь отправьте фотографии, по окончнии напишите 'Готово'",reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Готово"), types.KeyboardButton(text="Отмена")]],resize_keyboard=True))
        await state.set_state("model_photo")

@router.message(StateFilter("model_photo"))
async def model_handler(message: types.Message, state: FSMContext):
    
    sdata = await state.get_data()
    
    if message.text == "Отмена":
        await message.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    elif message.text == "Готово":
        photos_id = sdata.get("photos", [])
        bar = 0
        for i in photos_id:
            # await message.answer(i)
            await message.bot.download(file=i, destination=f"model/{i}.jpg")
            async with httpx.AsyncClient() as client:
                await client.post(f"http://{HOST}/model?name={sdata.get('name')}", json={"photo": base64.b64encode(open(f"model/{i}.jpg", "rb").read()).decode()})
                bar += 1
                await message.answer(f"Отправлено: {int(bar/len(photos_id) * 100)}%", reply_markup=types.ReplyKeyboardRemove())
    else:
        photo = message.photo[-1].file_id
        arr:list = sdata.get("photos", [])
        arr.append(photo)
        await state.update_data({"photos": arr})
        
        

