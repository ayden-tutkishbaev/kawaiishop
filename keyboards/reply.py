from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardBuilder

from database.queries import *
from utils.messages import *


def main_keyboard(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=REPLY_BUTTONS["catalogue"][language_code]),
             KeyboardButton(text=REPLY_BUTTONS["contacts"][language_code])],
            [KeyboardButton(text=REPLY_BUTTONS["feedback"][language_code]),
             KeyboardButton(text=REPLY_BUTTONS["about_us"][language_code])],
             [KeyboardButton(text=REPLY_BUTTONS["settings"][language_code])],
        ], resize_keyboard=True
    )
    return keyboard


def main_keyboard_for_admins(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=REPLY_BUTTONS["catalogue"][language_code]),
             KeyboardButton(text=REPLY_BUTTONS["contacts"][language_code])],
            [KeyboardButton(text=REPLY_BUTTONS["feedback"][language_code]),
             KeyboardButton(text=REPLY_BUTTONS["about_us"][language_code])],
             [KeyboardButton(text=REPLY_BUTTONS["settings"][language_code])],
            [KeyboardButton(text=ADMIN_PANEL["staff_button"][language_code])]
        ], resize_keyboard=True
    )
    return keyboard


def settings(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=REPLY_BUTTONS["change_lang"][language_code])],
            [KeyboardButton(text=MESSAGES["consumer_data"][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['admin_panel_leave'][language_code])]
        ], resize_keyboard=True
    )
    return keyboard


async def admins_list(language_code):
    builder = ReplyKeyboardBuilder()
    users = await get_admin_name()
    [builder.button(text=user) for user in users]
    builder.button(text=ADMIN_BUTTONS['add_staff'][language_code])
    builder.button(text=ADMIN_BUTTONS['back'][language_code])
    return builder.adjust(1).as_markup(resize_keyboard=True)


def creator_panel(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ADMIN_BUTTONS['manage_categories'][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['change_contacts'][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['change_bio'][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['newsletter'][language_code])],

            [KeyboardButton(text=ADMIN_BUTTONS["admin_list"][language_code])],  # must stand pre-last, no touch
            [KeyboardButton(text=ADMIN_BUTTONS['admin_panel_leave'][language_code])]  # must stand last, no touch
        ], resize_keyboard=True
    )
    return keyboard


def admins_panel(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=ADMIN_BUTTONS['manage_categories'][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['change_contacts'][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['change_bio'][language_code])],
            [KeyboardButton(text=ADMIN_BUTTONS['newsletter'][language_code])],

            [KeyboardButton(text=ADMIN_BUTTONS['admin_panel_leave'][language_code])]  # no touch
        ], resize_keyboard=True
    )
    return keyboard


# def categories_kb(language_code):
#     builder = ReplyKeyboardBuilder()
#     categories = get_categories()
#     if language_code == "eng":
#         [builder.button(text=category[0]).adjust(3) for category in categories]
#     elif language_code == "uzb":
#         [builder.button(text=category[1]).adjust(3) for category in categories]
#     elif language_code == "rus":
#         [builder.button(text=category[2]).adjust(3) for category in categories]
#     builder.adjust(3)
#     builder.row(KeyboardButton(text=ADMIN_BUTTONS['back'][language_code]))
#     return builder.as_markup(resize_keyboard=True)


def change_description(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="IN ENGLISH 🇬🇧")],
            [KeyboardButton(text="НА РУССКОМ 🇷🇺")],
            [KeyboardButton(text="O'ZBEKCHA 🇺🇿")],
            [KeyboardButton(text=ADMIN_BUTTONS['back'][language_code])]
        ], resize_keyboard=True
    )
    return keyboard


def contact_number(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MESSAGES['share_your_contact'][language_code], request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard


def cancel_operation(language_code):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MESSAGES['cancelled_action'][language_code])]
        ], resize_keyboard=True, one_time_keyboard=True
    )
    return keyboard


