from aiogram import types, Router, F
import json
router = Router()

@router.callback_query(F.data.startswith("notification"))
async def notification_handler(call: types.CallbackQuery):
    
    action = call.data.split(":")[1]
    match action:
        case "delete":
            await call.message.delete()
        case "unsubscribe":
            data = json.load(open("data.json"))
            if call.from_user.id in data["users"]:
                data["users"].remove(call.from_user.id)
                json.dump(data, open("data.json", "w"))
            await call.answer("Вы отписались от уведомлений")