from aiogram import Router, types
from aiogram.filters import Command
from asyncio import sleep
import httpx
import json
router = Router()


@router.message(Command(commands=["start"]))
async def start(message: types.Message):
    data = json.load(open("data.json"))
    if message.from_user.id not in data["users"]:
        data["users"].append(message.chat.id)
        json.dump(data, open("data.json", "w"))
    await message.answer("Привет! Теперь ты подписан на уведомления! Используй /menu для открытия меню")

        
        