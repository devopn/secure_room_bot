from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_notification_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="Просмотрено", callback_data="notification:delete"))
    builder.row(InlineKeyboardButton(text="Отписаться", callback_data="notification:unsubscribe"))
    builder.row(InlineKeyboardButton(text="В меню", callback_data="menu:menu"))
    return builder.as_markup()