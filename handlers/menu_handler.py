from typing import Union
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
import json
from keyboards.menu_keyboard import get_menu_keyboard

router = Router()


@router.message(Command("menu"))
@router.callback_query(F.data.startswith("menu"))
async def menu_handler(call: Union[types.CallbackQuery, types.Message], state: FSMContext):
    await state.clear()
    if isinstance(call, types.Message):
        await call.answer("Меню", reply_markup=get_menu_keyboard())
    else:
        
        action = call.data.split(":")[1]
        match action:
            case "menu":
                await call.answer()
                await call.message.answer("Меню", reply_markup=get_menu_keyboard())
            case "history":
                await call.message.answer("История оповещений")
            case "persons":
                await call.message.answer("Данные о людях")
            case "subscribe":
                data = json.load(open("data.json"))
                if call.from_user.id not in data["users"]:
                    data["users"].append(call.from_user.id)
                    json.dump(data, open("data.json", "w"))
                    await call.answer("Вы подписались на уведомления")
                else:
                    data["users"].remove(call.from_user.id)
                    json.dump(data, open("data.json", "w"))
                    await call.answer("Вы отписались от уведомлений")
            