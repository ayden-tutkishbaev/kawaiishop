from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, Contact
from aiogram.fsm.context import FSMContext

from FSM.states import *
from database.queries import *
import keyboards.inline as il
import keyboards.reply as rp
from utils.messages import *

from configs import ADMINS_ID, DEV_ID

user = Router()


@user.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await insert_data_to_language(message.chat.id)
    await message.answer(f"🇺🇿🇷🇺🇬🇧\n\n"
        f"<b>Choose a language</b>\n"
                         f"<b>Tilni tanlang</b>\n"
                         f"<b>Выберите язык</b>", reply_markup=il.languages_keyboard())


@user.callback_query(lambda callback: callback.data in ["rus", "eng", "uzb"])
async def set_language(callback: CallbackQuery, state: FSMContext) -> None:
    await update_data_to_language(callback.message.chat.id, callback.data)
    language_code = await get_user_language(callback.message.chat.id)
    # print(language_code)
    await callback.message.delete()
    if callback.message.chat.id in await get_admin_id() + ADMINS_ID + DEV_ID:
        await callback.message.answer(MESSAGES["welcome_message"][language_code],
                                      reply_markup=rp.main_keyboard_for_admins(language_code))
    else:
        if callback.message.chat.id in await get_all_consumers():
            await callback.message.answer(MESSAGES["welcome_message"][language_code],
                                          reply_markup=rp.main_keyboard(language_code))
        else:
            await state.set_state(UserRegistration.contact)
            await callback.message.answer(f"{MESSAGES['ask_contact'][language_code]}", reply_markup=rp.contact_number(language_code))


@user.callback_query(F.data == 'change_profile')
async def alter_profile(callback: CallbackQuery, state: FSMContext) -> None:
    language_code = await get_user_language(callback.message.chat.id)
    await state.set_state(UserRegistration.contact)
    await callback.message.answer(MESSAGES["ask_contact"][language_code], reply_markup=rp.contact_number(language_code))


@user.message(UserRegistration.contact)
async def get_contact(message: Message, state: FSMContext):
    if message.chat.id not in await get_all_consumers():
        await insert_consumer_data(message.chat.id, message.from_user.full_name)
    language_code = await get_user_language(message.chat.id)
    if message.contact:
        await state.update_data(contact=f'+{message.contact.phone_number}')
    elif message.text:
        await state.update_data(contact=message.text)
    await state.set_state(UserRegistration.full_name)
    await message.answer(MESSAGES["ask_fullname"][language_code])


@user.message(UserRegistration.full_name)
async def get_fullname(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    await insert_other_consumer_data(message.chat.id, data['contact'], data['full_name'])
    await message.answer(MESSAGES['success_reg'][language_code], reply_markup=rp.main_keyboard(language_code))
    await state.clear()


@user.message(lambda message: message.text in ["Back ⬅️",
"Назад ⬅️",
"Ortga ⬅️",
"Back to main menu ⬅️",
"Назад в главное меню ⬅️",
"Asosiy menyuga qaytish ⬅️"])
async def back_to_main_menu(message: Message):
    language_code = await get_user_language(message.chat.id)
    if message.chat.id in await get_admin_id() + ADMINS_ID + DEV_ID:
        await message.answer(MESSAGES["main_menu"][language_code],
                             reply_markup=rp.main_keyboard_for_admins(language_code))
    else:
        await message.answer(MESSAGES["main_menu"][language_code],
                             reply_markup=rp.main_keyboard(language_code))


@user.message(F.text.in_(list(REPLY_BUTTONS['settings'].values())))
async def settings_m(message: Message):
    language_code = await get_user_language(message.chat.id)
    await message.answer(REPLY_BUTTONS["settings_page"][language_code], reply_markup=rp.settings(language_code))


@user.message(F.text.in_(list(REPLY_BUTTONS['change_lang'].values())))
async def change_lang(message: Message):
    await command_start_handler(message)


@user.message(F.text.in_(list(REPLY_BUTTONS['contacts'].values())))
async def contacts_handler(message: Message):
    all_contacts = await get_contacts()
    await message.answer(all_contacts)


@user.message(F.text.in_(list(REPLY_BUTTONS['feedback'].values())))
async def leave_feedback(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.set_state(Feedback.message)
    await message.answer(ADMIN_BUTTONS['feedback'][language_code], reply_markup=rp.cancel_operation(language_code))


@user.message(Feedback.message)
async def feedback_saved(message: Message, state: FSMContext, bot: Bot) -> None:
    language_code = await get_user_language(message.chat.id)
    admins = await get_admin_id() + ADMINS_ID + DEV_ID
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        if message.chat.id in await get_admin_id() + ADMINS_ID + DEV_ID:
            await message.answer(MESSAGES["main_menu"][language_code],
                                          reply_markup=rp.main_keyboard_for_admins(language_code))
        else:
            await message.answer(MESSAGES["main_menu"][language_code],
                                          reply_markup=rp.main_keyboard(language_code))
    else:
        await state.set_state(Feedback.message)
        try:
            for admin in admins:
                if message.from_user.username:
                    await bot.send_message(chat_id=admin,
                                           text=f"⬇️ <b>{ADMIN_BUTTONS['feedback_received'][language_code]} @{message.from_user.username}</b>")
                else:
                    await bot.send_message(chat_id=admin,
                                           text=f"⬇️ <b>{ADMIN_BUTTONS['feedback_received'][language_code]} <i>{message.from_user.full_name}</i></b>")
                await message.send_copy(chat_id=admin, reply_markup=il.admin_answer(message.chat.id, language_code))
            await message.answer(ADMIN_PANEL['success'][language_code], reply_markup=rp.main_keyboard(language_code))
            await state.clear()
        except:
            await message.answer(ADMIN_BUTTONS['feedback_error'][language_code], reply_markup=rp.main_keyboard(language_code))


@user.message(F.text.in_(list(REPLY_BUTTONS['catalogue'].values())))
async def catalogue_handler(message: Message) -> None:
    language_code = await get_user_language(message.chat.id)
    await message.answer(REPLY_BUTTONS['catalogue'][language_code], reply_markup=await il.categories_kb(language_code))


@user.callback_query(F.data.startswith("usercategory_"))
async def categories_list_user(callback: CallbackQuery):
    category_name = ' '.join(callback.data.split('_')[2:])
    category_id = int(callback.data.split('_')[1])
    await callback.message.edit_text(text=category_name, reply_markup=await il.goods_per_category(category_id))


@user.callback_query(F.data.startswith("userkategoriya_"))
async def categories_list_user(callback: CallbackQuery):
    category_name = ' '.join(callback.data.split('_')[2:])
    category_id = int(callback.data.split('_')[1])
    await callback.message.edit_text(text=category_name, reply_markup=await il.goods_per_category(category_id))


@user.callback_query(F.data.startswith("userkategoria_"))
async def categories_list_user(callback: CallbackQuery):
    category_name = ' '.join(callback.data.split('_')[2:])
    category_id = int(callback.data.split('_')[1])
    await callback.message.edit_text(text=category_name, reply_markup=await il.goods_per_category(category_id))


@user.callback_query(F.data == 'user_back_to_categories')
async def back_to_catalogue(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    await callback.message.edit_text(REPLY_BUTTONS['catalogue'][language_code], reply_markup=await il.categories_kb(language_code))


@user.callback_query(F.data.startswith("good_"))
async def goods(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = int(callback.data.split('_')[1])
    good = await get_good(good_id)
    await callback.message.answer_photo(caption=f"${good[2]}\n\n{good[0]}\n\n{good[1]}", photo=good[3],
                                        reply_markup=il.contact_seller(language_code, good_id))


@user.message(F.text.in_(list(REPLY_BUTTONS['about_us'].values())))
async def about_us(message: Message):
    language_code = await get_user_language(message.chat.id)
    description = await get_all_descriptions()
    if language_code == "eng":
        await message.answer(description[2])
    if language_code == "rus":
        await message.answer(description[1])
    if language_code == "uzb":
        await message.answer(description[0])


@user.message(F.text.in_(list(MESSAGES['consumer_data'].values())))
async def my_data(message: Message):
    consumer_data = await get_consumer_data(message.chat.id)
    language = await get_user_language(message.chat.id)
    await message.answer(f"{consumer_data[0]},\n\n<b>{MESSAGES['consumer_fullname'][language]}</b>\n<i>{consumer_data[1]}</i>\n<b>{MESSAGES['consumer_contact'][language]}</b>\n<i>{consumer_data[2]}</i>",
                         reply_markup=il.change_consumer_data(language))


@user.callback_query(F.data.startswith('contact_seller'))
async def contact_seller(callback: CallbackQuery, bot: Bot):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = int(callback.data.split('_')[-1])
    good = await get_good(good_id)
    consumer_data = await get_consumer_data(callback.message.chat.id)
    admins = ADMINS_ID + DEV_ID + await get_admin_id()

    for admin in admins:
        await bot.send_message(admin,
                                f"<b>{MESSAGES['good_interested'][language_code]}</b>\n{good[0]}\n\n<b>{MESSAGES['clients_phone_number'][language_code]}</b> <i>{consumer_data[2]}</i>\n<b>{MESSAGES['clients_full_name'][language_code]}</b> <i>{consumer_data[1]}</i>")

    await bot.send_message(callback.message.chat.id, MESSAGES['obtain_request'][language_code])

    await callback.answer()