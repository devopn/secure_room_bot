from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_history_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Предыдущий", callback_data="history:prev"),
        InlineKeyboardButton(text="Следующий", callback_data="history:next")
        )
    builder.row(InlineKeyboardButton(text="Получить json", callback_data="history:get_data"))
    builder.row(InlineKeyboardButton(text="В меню", callback_data="menu:menu"))
    return builder.as_markup()