from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_person_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Предыдущий", callback_data="person:prev"),
        InlineKeyboardButton(text="Следующий", callback_data="person:next")
    )
    builder.row(InlineKeyboardButton(text="В меню", callback_data="menu:menu"))
    return builder.as_markup()