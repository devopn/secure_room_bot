import base64
from aiogram import Bot, Dispatcher
import asyncio
import aiogram
import httpx
from handlers.command_handler import router as command_router
from handlers.notification_handler import router as notification_router
from handlers.menu_handler import router as menu_router
from handlers.history_handler import router as history_router
from handlers.persons_handler import router as persons_router
from handlers.model_handler import router as model_handler
import logging
from keyboards.notification_keyboard import get_notification_keyboard
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename="bot.log")

from config import config
HOST = config.host
bot = Bot(token="7248761303:AAGORKQbU3cV8jJCPPG7wyc-vGX3s1A-CFg")
dp = Dispatcher()
dp.include_routers(command_router,notification_router,  menu_router, history_router, persons_router, model_handler)



async def main():
    
    await bot.delete_webhook(drop_pending_updates=False)
    task = asyncio.create_task(coro=notificate(delay=5))
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def notificate(delay):
    while True:
        try:
            print("notificate")
            async with httpx.AsyncClient() as client:
                new_meets = await client.get(f"http://{HOST}/meet/unwatched", timeout=10)
                if (new_meets.status_code == 200) and (len(new_meets.json()) > 0):
                    # print(new_meets.json())
                    users = json.load(open("data.json"))
                    data = new_meets.json()
                    for meet in data:
                        names = meet["names"] # {name:score}
                        names = [(k, v) for k, v in names.items()]
                        names = sorted(names, key=lambda x: x[1], reverse=True)
                        sum_score = sum([name[1] for name in names])
                        names = [f"{name[0]} - {int((name[1]/sum_score) * 100)}%" for name in names]
                        
                        for user in users["users"]:
                            b64photo = meet["photo"]
                            photo = aiogram.types.BufferedInputFile(base64.b64decode(b64photo), "swap")
                            await bot.send_photo(user, photo=photo,caption="Возможно на этой фотографии: " + ", ".join(names), reply_markup=get_notification_keyboard())
            await asyncio.sleep(delay)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())

    
    
    
