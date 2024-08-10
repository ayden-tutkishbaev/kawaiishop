from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardBuilder
from utils.messages import *
from database.queries import *


def languages_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Русский 🇷🇺", callback_data="rus")],
            [InlineKeyboardButton(text="English 🇬🇧", callback_data="eng")],
            [InlineKeyboardButton(text="O‘zbekcha 🇺🇿", callback_data="uzb")]
        ]
    )
    return keyboard


def admin_deletion(language_code):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ADMIN_BUTTONS['admin_delete'][language_code], callback_data="delete_admin")],
            [InlineKeyboardButton(text=ADMIN_BUTTONS['back'][language_code], callback_data="back_to_admins")]
        ]
    )
    return keyboard


async def category_management(language_code, category_id):
    builder = InlineKeyboardBuilder()
    goods = await get_goods_by_category(category_id)
    [builder.add(InlineKeyboardButton(text=good[0], callback_data=f'admingoods_{good[1]}')) for good in goods]
    builder.adjust(3)

    builder.row(InlineKeyboardButton(text=ADMIN_BUTTONS['change'][language_code], callback_data=f"alter_category_{category_id}")),
    builder.row(InlineKeyboardButton(text=ADMIN_PANEL["add_good"][language_code], callback_data=f"add_a_good_{category_id}")),
    builder.row(InlineKeyboardButton(text=ADMIN_BUTTONS['admin_delete'][language_code], callback_data=f"delete_category_{category_id}")),
    builder.row(InlineKeyboardButton(text=ADMIN_BUTTONS['back'][language_code], callback_data=f"from_category_back_to_categories")),
    return builder.as_markup()


async def categories_kb(language_code):
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    if language_code == "eng":
        [builder.add(InlineKeyboardButton(text=category[0], callback_data=f"usercategory_{category[3]}_{category[0]}")) for category in categories]
    elif language_code == "uzb":
        [builder.add(InlineKeyboardButton(text=category[1], callback_data=f"userkategoriya_{category[3]}_{category[1]}")) for category in categories]
    elif language_code == "rus":
        [builder.add(InlineKeyboardButton(text=category[2], callback_data=f"userkategoria_{category[3]}_{category[2]}")) for category in categories]
    builder.adjust(3)

    return builder.as_markup()


async def categories_selection(language_code):
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    if language_code == "eng":
        [builder.add(InlineKeyboardButton(text=category[0], callback_data=f"addcategory_{category[3]}")) for category in categories]
    elif language_code == "uzb":
        [builder.add(InlineKeyboardButton(text=category[1], callback_data=f"addcategory_{category[3]}")) for category in categories]
    elif language_code == "rus":
        [builder.add(InlineKeyboardButton(text=category[2], callback_data=f"addcategory_{category[3]}")) for category in categories]
    builder.row(InlineKeyboardButton(text=MESSAGES['cancelled_action'][language_code], callback_data=f"cancelled_action"))
    builder.adjust(3)

    # builder.row(InlineKeyboardButton(text=ADMIN_BUTTONS['back'][language_code], callback_data="back_to_menu"))
    return builder.as_markup()


async def for_admins_categories_kb(language_code):
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    if language_code == "eng":
        [builder.add(InlineKeyboardButton(text=category[0], callback_data=f"admincategory_{category[3]}_{category[0]}")) for category in categories]
    elif language_code == "uzb":
        [builder.add(InlineKeyboardButton(text=category[1], callback_data=f"adminkategoriya_{category[3]}_{category[1]}")) for category in categories]
    elif language_code == "rus":
        [builder.add(InlineKeyboardButton(text=category[2], callback_data=f"adminkategoria_{category[3]}_{category[2]}")) for category in categories]
    builder.adjust(3)

    builder.row(InlineKeyboardButton(text="➕", callback_data="add_category"))
    builder.row(InlineKeyboardButton(text="⬅️", callback_data="back_to_menu"))
    return builder.as_markup()


async def goods_per_category(category_id):
    builder = InlineKeyboardBuilder()
    goods = await get_goods_by_category(category_id)
    [builder.add(InlineKeyboardButton(text=good[0], callback_data=f'good_{good[1]}')) for good in goods]
    builder.adjust(3)
    builder.row(InlineKeyboardButton(text="⬅️", callback_data="user_back_to_categories"))
    return builder.as_markup()


def manage_good(good_id, language_code):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTONS['change_title'][language_code], callback_data=f"change_good_title_{good_id}")],
            [InlineKeyboardButton(text=BUTTONS['change_desc'][language_code], callback_data=f"change_desc_{good_id}")],
            [InlineKeyboardButton(text=BUTTONS['change_photo'][language_code], callback_data=f"change_photo_{good_id}")],
            [InlineKeyboardButton(text=BUTTONS['change_category'][language_code], callback_data=f"change_category_{good_id}")],
            [InlineKeyboardButton(text=BUTTONS['change_cost'][language_code], callback_data=f"change_price_{good_id}")],
            [InlineKeyboardButton(text=f'❌ {BUTTONS["delete_good"][language_code]}', callback_data=f"good_delete_{good_id}")],
            # [InlineKeyboardButton(text=BUTTONS['back_to_categories'][language_code], callback_data=f"back_to_adminkategoria_{category_id}")],
        ]
    )
    return keyboard


def deletion_confirmation(category_id, language_code):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTONS['confirmation'][language_code], callback_data=f"confirmed_delete_category_{category_id}")],
            [InlineKeyboardButton(text='⬅️', callback_data=f"from_category_back_to_categories")]
        ]
    )
    return keyboard


def deletion_confirmation_good(good_id, language_code):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=BUTTONS['confirmation'][language_code], callback_data=f"confirmed_delete_good_{good_id}")],
            [InlineKeyboardButton(text='⬅️', callback_data=f"back_to_good_{good_id}")]
        ]
    )
    return keyboard


def change_consumer_data(language_code):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MESSAGES['consumer_data_change'][language_code], callback_data='change_profile')]
        ]
    )
    return keyboard


def contact_seller(language_code, category_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=MESSAGES['contact_seller'][language_code],
                                  callback_data=f'contact_seller_{category_id}')]
        ]
    )
    return keyboard


def admin_answer(sender_id, language_code):
    button = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=BUTTONS['answer_to_feedback'][language_code],
                                                                         callback_data=f"answer_to_{sender_id}")]])

    return button