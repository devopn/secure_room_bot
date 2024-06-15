import json
from typing import Union
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import httpx
import base64
import datetime
from keyboards.history_keyboard import get_history_keyboard
router = Router()
from config import config
HOST = config.host

async def create_answer(message:Union[types.Message, types.CallbackQuery], data:dict):

    names = data["names"] # {name:score}
    names = [(k, v) for k, v in names.items()]
    names = sorted(names, key=lambda x: x[1], reverse=True)
    sum_score = sum([name[1] for name in names])
    names = [f"{name[0]} - {int((name[1]/sum_score) * 100)}%" for name in names]
    print(names)
    dt = datetime.datetime.fromisoformat(data["datetime"])
    text = f"Возможно на этой фотографии: {','.join(names)}\n{dt.strftime('%d.%m.%Y %H:%M')}\n#{data['id']}"
    b64photo = data["photo"]
    photo = types.BufferedInputFile(base64.b64decode(b64photo), "swap")

    if isinstance(message, types.Message):
        await message.answer_photo(caption=text, photo = photo, reply_markup=get_history_keyboard())
    else:
        
        await message.message.edit_media(media=types.InputMediaPhoto(media=photo, caption=text), reply_markup=get_history_keyboard())
        # await message.message.edit_caption(text, reply_markup=get_history_keyboard())

@router.callback_query(F.data.startswith("history"))
async def history_handler(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    match action:
        case "prev":
            async with httpx.AsyncClient() as client:
                state_data = await state.get_data()
                meet = await client.get(f"http://{HOST}/meet/{state_data['currentId']-1}")
                if meet.status_code == 200:
                    data = meet.json()
                    await state.set_data({"currentId": data["id"]})
                    await create_answer(message=call, data=data)
                else:
                    await call.answer("Нет оповещений")
        case "next":
            async with httpx.AsyncClient() as client:
                state_data = await state.get_data()
                meet = await client.get(f"http://{HOST}/meet/{state_data['currentId']+1}")
                if meet.status_code == 200:
                    data = meet.json()
                    await state.set_data({"currentId": data["id"]})
                    await create_answer(message=call, data=data)
                else:
                    await call.answer("Нет оповещений")
        case "get_data":
            async with httpx.AsyncClient() as client:
                all_meets = await client.get(f"http://{HOST}/meet/all?limit=-1")
                if all_meets.status_code == 200:
                    data = all_meets.json()
                    await call.message.answer("Файл начал формироваться, если данных много, на это может потребоваться некоторое время, можете продолжать пользоваться ботом")
                    filedata = types.BufferedInputFile(json.dumps(data).encode(), "meets.json")
                    await call.message.answer_document(document=filedata, caption=f"Всего оповещений: {len(data)}")
                    await call.answer("Данные отправлены")
        case "history":
            async with httpx.AsyncClient() as client:
                last_meet = await client.get(f"http://{HOST}/meet/all?limit=1")
                if last_meet.status_code == 200:
                    data = last_meet.json()
                    if len(data) == 0:
                        await call.answer("Нет оповещений")
                        return
                    await state.set_data({"currentId": data[0]["id"]})
                    await create_answer(message=call.message, data=data[0])
                    await call.answer()
                else:
                    await call.answer("Нет оповещений")