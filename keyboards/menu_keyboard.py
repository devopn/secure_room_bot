from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.row(InlineKeyboardButton(text="История оповещений", callback_data="history:history"))
    builder.row(InlineKeyboardButton(text="Данные о людях", callback_data="persons:persons"))
    builder.row(InlineKeyboardButton(text="Загрузить свою модель", callback_data="model:model"))
    builder.row(InlineKeyboardButton(text="Подписаться/отписаться", callback_data="menu:subscribe"))

    return builder.as_markup()
