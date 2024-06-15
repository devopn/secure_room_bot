from typing import Union
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
import httpx
import json
import datetime
import base64
from keyboards.person_keyboard import get_person_keyboard
from config import config
HOST = config.host
router = Router()

async def make_answer(message: Union[types.Message, types.CallbackQuery], data:dict): 
    async with httpx.AsyncClient() as client:
        meet = await client.get(f"http://{HOST}/meet/person/{data['id']}")
        meet_data = meet.json()
        print(meet_data)
        b64photo = meet_data["photo"]
        photo = types.BufferedInputFile(base64.b64decode(b64photo), "swap")
        text = f"Имя: {data['name']}\nДата последней встречи: {datetime.datetime.fromisoformat(meet_data['datetime']).strftime('%d.%m.%Y %H:%M')}\n#{data['id']}"
        if isinstance(message, types.Message):
            await message.answer_photo(caption=text, photo=photo, reply_markup=get_person_keyboard())
        else:
            await message.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=text), reply_markup=get_person_keyboard())

@router.callback_query(F.data.startswith("person"))
async def persons_handler(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    # Я решил не менять структуру своего кода, хотя тут это возможно имело бы смысл
    match action:
        case "persons":
            async with httpx.AsyncClient() as client:
                last_people = await client.get(f"http://{HOST}/person/all?limit=1")
                if last_people.status_code == 200:
                    data = last_people.json()[0]
                    await state.set_data({"currentId": data["id"]})
                    await make_answer(message=call.message, data=data)
                    await call.answer()
                else:
                    await call.answer("Нет людей")
                    
        case "next":
            state_data = await state.get_data()
            async with httpx.AsyncClient() as client:
                people = await client.get(f"http://{HOST}/person/{state_data['currentId']+1}")
                if people.status_code == 200:
                    data = people.json()
                    await state.set_data({"currentId": data["id"]})
                    await make_answer(message=call, data=data)
                    await call.answer()
                else:
                    await call.answer("Конец списка")
        case "prev":
            state_data = await state.get_data()
            async with httpx.AsyncClient() as client:
                people = await client.get(f"http://{HOST}/person/{state_data['currentId']-1}")
                if people.status_code == 200:
                    data = people.json()
                    await state.set_data({"currentId": data["id"]})
                    await make_answer(message=call, data=data)
                    await call.answer()
                else:
                    await call.answer("Конец списка")
        case "none":
            await call.answer()