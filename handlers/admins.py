from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from FSM.states import *
from utils.utils import *
from database.queries import *

import keyboards.reply as rp
import keyboards.inline as il
from utils.messages import *

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SYSTEM_ADMINS = [int(dotenv['ADMIN_1_ID']), int(dotenv['ADMIN_2_ID']), int(dotenv['DEV_ID'])]

admin = Router()


@admin.message(Admin(), lambda message: message.text in ["For staff 🔐",
"Для персонала 🔐",
"Xodimlar uchun 🔐",
                                                         "Back ⬅️",
                                                         "Назад ⬅️",
                                                         "Ortga ⬅️",
                                                         "/admin"
                                                         ])
async def admin_mode(message: Message) -> None:
    language_code = await get_user_language(message.chat.id)
    if message.chat.id in SYSTEM_ADMINS:
        await message.answer(ADMIN_PANEL['staff_welcome'][language_code],
                             reply_markup=rp.creator_panel(language_code))
    else:
        await message.answer(ADMIN_PANEL['staff_welcome'][language_code],
                             reply_markup=rp.admins_panel(language_code))


@admin.message(MainAdmin(), F.text.in_(list(ADMIN_BUTTONS['add_staff'].values())))
async def add_staff(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.set_state(AddAdminStaff.telegram_id)
    await message.answer(ADMIN_PANEL['add_staff'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(MainAdmin(), AddAdminStaff.telegram_id)
async def add_staff_name(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.creator_panel(language_code))
    else:
        language_code = await get_user_language(message.chat.id)
        await state.update_data(telegram_id=int(message.text))
        await state.set_state(AddAdminStaff.name)
        await message.answer(ADMIN_PANEL['add_staff_name'][language_code])


@admin.message(MainAdmin(), AddAdminStaff.name)
async def add_staff_to_db(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.update_data(name=message.text)
    data = await state.get_data()
    await add_admin_to_db(data['telegram_id'], data['name'])
    await state.clear()
    await message.answer(ADMIN_PANEL['success'][language_code], reply_markup=await rp.admins_list(language_code))


@admin.message(MainAdmin(), F.text.in_(list(ADMIN_BUTTONS['admin_list'].values())))
async def admins_display(message: Message) -> None:
    language_code = await get_user_language(message.chat.id)
    await message.answer(ADMIN_PANEL['admins_list'][language_code], reply_markup=await rp.admins_list(language_code))


@admin.message(Managers())
async def admin_deletion(message: Message) -> None:
    language_code = await get_user_language(message.chat.id)
    await message.answer(f"{message.text}", reply_markup=il.admin_deletion(language_code))


@admin.callback_query(MainAdmin(), F.data == 'back_to_admins')
async def back_to_menu(callback: CallbackQuery) -> None:
    await admins_display(callback.message)
    await callback.message.delete()
    # await callback.message.answer(callback.message.text)


@admin.callback_query(MainAdmin(), F.data == 'delete_admin')
async def delete_admin(callback: CallbackQuery) -> None:
    language_code = await get_user_language(callback.message.chat.id)
    await delete_admin_from_table(callback.message.text)
    await callback.message.answer(ADMIN_PANEL['success'][language_code], reply_markup=await rp.admins_list(language_code))
    await callback.message.delete()


@admin.callback_query(Admin(), F.data == 'add_category')
async def category_addition(callback: CallbackQuery, state: FSMContext) -> None:
    language_code = await get_user_language(callback.message.chat.id)
    await state.set_state(AddCategory.title_eng)
    await callback.message.answer(ADMIN_PANEL['start'][language_code])
    await callback.message.answer(ADMIN_PANEL['category_add_eng'][language_code],
                                  reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AddCategory.title_eng)
async def add_category_eng(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=await il.for_admins_categories_kb(language_code))
    else:
        await state.update_data(title_eng=message.text)
        await state.set_state(AddCategory.title_uzb)
        await message.answer(ADMIN_PANEL['category_add_uzb'][language_code])


@admin.message(Admin(), AddCategory.title_uzb)
async def add_category_uzb(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.update_data(title_uzb=message.text)
    await state.set_state(AddCategory.title_rus)
    await message.answer(ADMIN_PANEL['category_add_rus'][language_code])


@admin.message(Admin(), AddCategory.title_rus)
async def add_category_rus(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.update_data(title_rus=message.text)
    data = await state.get_data()
    await category_add(data['title_eng'], data['title_uzb'], data['title_rus'])
    await message.answer(ADMIN_PANEL['success'][language_code], reply_markup=await il.for_admins_categories_kb(language_code))
    await state.clear()


@admin.message(Admin(), F.text.in_(list(ADMIN_BUTTONS['newsletter'].values())))
async def newsletter(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.set_state(NewsLetter.message)
    await message.answer(ADMIN_PANEL['newsletter'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), NewsLetter.message)
async def sending_to_all(message: Message, state: FSMContext, bot: Bot) -> None:
    language_code = await get_user_language(message.chat.id)
    users = await get_all_chats()
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        for user in users:
            try:
                await message.send_copy(chat_id=user)
            except:
                await message.answer(ADMIN_BUTTONS['feedback_error'][language_code])
        await message.answer(ADMIN_PANEL['success'][language_code], reply_markup=rp.admins_panel(language_code))
        await state.clear()


@admin.message(Admin(), F.text.in_(list(ADMIN_BUTTONS['change_bio'].values())))
async def change_description_main(message: Message):
    language_code = await get_user_language(message.chat.id)
    await message.answer("⬇️⬇️⬇️", reply_markup=rp.change_description(language_code))


@admin.message(Admin(), F.text == "НА РУССКОМ 🇷🇺")
async def alter_rus_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.set_state(RusDescription.message)
    await message.answer("Отправьте ваше описание: ", reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), RusDescription.message)
async def insert_rus_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.change_description(language_code))
    else:
        await state.update_data(message=message.text)
        data = await state.get_data()
        await update_rus_description(data['message'])
        await state.clear()
        await message.answer("Операция прошла успешно!", reply_markup=rp.change_description(language_code))


@admin.message(Admin(), F.text == "IN ENGLISH 🇬🇧")
async def alter_eng_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.set_state(EngDescription.message)
    await message.answer("Send your description: ", reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), EngDescription.message)
async def insert_eng_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.change_description(language_code))
    else:
        await state.update_data(message=message.text)
        data = await state.get_data()
        await update_eng_description(data['message'])
        await state.clear()
        await message.answer("Operation is successful!", reply_markup=rp.change_description(language_code))


@admin.message(Admin(), F.text == "O'ZBEKCHA 🇺🇿")
async def alter_uzb_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.set_state(UzbDescription.message)
    await message.answer("Tavsifingizni jo'nating", reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), UzbDescription.message)
async def insert_uzb_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.change_description(language_code))
    else:
        await state.update_data(message=message.text)
        data = await state.get_data()
        await update_uzb_description(data['message'])
        await state.clear()
        await message.answer("Operatsiya muvaffaqiyatli o'tdi!",
                             reply_markup=rp.change_description(language_code))


@admin.message(Admin(), F.text.in_(list(ADMIN_BUTTONS['change_contacts'].values())))
async def update_contacts_handler(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.set_state(ContactsEdit.message)
    await message.answer(ADMIN_PANEL['contacts_update'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), ContactsEdit.message)
async def insert_contacts(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        await state.update_data(message=message.text)
        data = await state.get_data()
        await update_contacts(data['message'])

        await message.answer(ADMIN_PANEL['success'][language_code], reply_markup=rp.admins_panel(language_code))
        await state.clear()


@admin.message(Admin(), F.text.in_(list(ADMIN_BUTTONS['manage_categories'].values())))
async def manage_categories(message: Message):
    language_code = await get_user_language(message.chat.id)
    await message.answer(ADMIN_PANEL['categories_display'][language_code],
                         reply_markup=await il.for_admins_categories_kb(language_code))


# @admin.callback_query(Admin(), F.data.startswith("goodcategory_"))
# async def goods_per_category_admin(callback: CallbackQuery):
#     language_code = get_user_language(callback.message.chat.id)
#     category_id = callback.data.split('_')[1]
#     await callback.message.edit_text("All goods:", reply_markup=il.goods_per_category_admin(category_id))


@admin.callback_query(Admin(), F.data.startswith("adminkategoria_"))
async def categories_list_ru(callback: CallbackQuery):
    print(callback.data)
    category_name = ' '.join(callback.data.split('_')[2:])
    category_id = int(callback.data.split('_')[1])
    language_code = await get_user_language(callback.message.chat.id)
    await callback.message.edit_text(f"{category_name}",
                                     reply_markup=await il.category_management(language_code, category_id))


@admin.callback_query(Admin(), F.data.startswith("adminkategoriya_"))
async def categories_list_uz(callback: CallbackQuery):
    category_name = ' '.join(callback.data.split('_')[2:])
    category_id = int(callback.data.split('_')[1])
    language_code = await get_user_language(callback.message.chat.id)
    print(category_id)
    await callback.message.edit_text(f"{category_name}",
                                     reply_markup=await il.category_management(language_code, category_id))


@admin.callback_query(Admin(), F.data.startswith("admincategory_"))
async def categories_list_en(callback: CallbackQuery):
    category_name = ' '.join(callback.data.split('_')[2:])
    category_id = int(callback.data.split('_')[1])
    print(category_id)
    language_code = await get_user_language(callback.message.chat.id)
    await callback.message.edit_text(f"{category_name}",
                                     reply_markup=await il.category_management(language_code, category_id))


@admin.callback_query(F.data.startswith("admingoods_"))
async def goods(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = int(callback.data.split('_')[1])
    good = await get_good(good_id)
    await callback.message.answer_photo(caption=f"${good[2]}\n\n{good[0]}\n\n{good[1]}", photo=good[3],
                                        reply_markup=il.manage_good(good_id, language_code))


@admin.callback_query(Admin(), F.data.startswith('delete_category'))
async def delete_category_confirmation(callback: CallbackQuery):
    print(callback.data)
    category_id = callback.data.split('_')[2]
    print(category_id)
    language_code = await get_user_language(callback.message.chat.id)
    await callback.message.edit_text(text=REPLY_BUTTONS['delete_category_confirm'][language_code],
                                     reply_markup=il.deletion_confirmation(category_id, language_code))


@admin.callback_query(Admin(), F.data.startswith('confirmed_delete_category_'))
async def delete_category_handler(callback: CallbackQuery):
    category_id = int(callback.data.split('_')[-1])
    language_code = await get_user_language(callback.message.chat.id)
    await delete_category_from_table(category_id)
    await callback.message.edit_text(text=REPLY_BUTTONS['deleted'][language_code],
                                     reply_markup=await il.for_admins_categories_kb(language_code))


@admin.callback_query(Admin(), F.data == 'from_category_back_to_categories')
async def back_to_categories(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    await callback.message.answer(ADMIN_PANEL['categories_display'][language_code],
                                  reply_markup=await il.for_admins_categories_kb(language_code))


# @admin.callback_query(Admin(), F.data.startswith('back_to_'))
# async def back_to_category(callback: CallbackQuery):
#     category_data = callback.data.split('_')[2:]
#     category = '_'.join(category_data)
#     print(category)
#     language_code = get_user_language(callback.message.chat.id)
#     if language_code == 'rus':
#         await categories_list_ru(callback)
#     if language_code == 'eng':
#         await categories_list_en(callback)
#     if language_code == 'uzb':
#         await categories_list_uz(callback)


@admin.callback_query(Admin(), F.data == 'back_to_menu')
async def back_to_categories(callback: CallbackQuery):
    await callback.message.delete()
    await admin_mode(callback.message)


@admin.callback_query(Admin(), F.data.startswith('add_a_good'))  # TODO: think
async def add_a_good_start(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    print(callback.data)
    category_id = int(callback.data.split("_")[-1])
    print(category_id)
    await state.set_state(AddGoods.category)
    await state.update_data(category=category_id)
    await state.set_state(AddGoods.title)
    await callback.message.answer(ADMIN_PANEL['good_title'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AddGoods.title)
async def add_title_to_goods(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=await il.for_admins_categories_kb(language_code))
    else:
        await state.update_data(title=message.text)
        await state.set_state(AddGoods.photo)
        await message.answer(ADMIN_PANEL['good_photo'][language_code])


@admin.message(Admin(), AddGoods.photo, F.photo)
async def add_photo_to_goods(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.update_data(photo=message.photo[-1].file_id)
    await state.set_state(AddGoods.description)
    await message.answer(ADMIN_PANEL['good_desc'][language_code])


@admin.message(Admin(), AddGoods.photo, ~F.photo)
async def add_photo_incorrect(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await message.answer(ADMIN_PANEL['not_photo'][language_code])


@admin.message(Admin(), AddGoods.description)
async def add_description_to_goods(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    await state.update_data(description=message.text)
    await state.set_state(AddGoods.price)
    await message.answer(ADMIN_PANEL['good_cost'][language_code])


@admin.message(Admin(), AddGoods.price)
async def add_price_to_goods(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text.isdigit():
        price = int(message.text)
        await state.update_data(price=price)
    else:
        await message.answer(ADMIN_PANEL['not_digit_price'][language_code])
    data = await state.get_data()
    print(data)
    await insert_good_to_table(data['title'], data['description'], data['category'], data['price'], data['photo'])
    await message.answer(ADMIN_PANEL['main_menu'][language_code],
                         reply_markup=await rp.admins_panel(language_code))
    await message.answer(ADMIN_PANEL['good_added_success'][language_code],
                         reply_markup=await il.for_admins_categories_kb(language_code))
    await state.clear()


@admin.callback_query(Admin(), F.data.startswith("change_good_title_"))
async def good_change_title(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    print(callback.data)
    good_id = callback.data.split("_")[-1]
    await state.set_state(AlterGoodTitle.id)
    await state.update_data(id=int(good_id))
    await state.set_state(AlterGoodTitle.title)
    await callback.message.answer(ADMIN_PANEL['good_title'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AlterGoodTitle.title)
async def insert_new_title(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        await state.update_data(title=message.text)
        data = await state.get_data()
        await change_good_title(data['title'], data['id'])
        good_data = await get_good(data['id'])
        await message.answer_photo(caption=f"${good_data[2]}\n\n{good_data[0]}\n\n{good_data[1]}", photo=good_data[3],
                                   reply_markup=il.manage_good(data['id'], language_code))
        await state.clear()
        await message.answer(ADMIN_PANEL['success'][language_code],
                                      reply_markup=rp.admins_panel(language_code))


@admin.callback_query(Admin(), F.data.startswith("good_delete_"))
async def good_deletion(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = callback.data.split("_")[-1]
    # delete_good(good_id)
    # await callback.message.delete()
    await callback.message.answer(REPLY_BUTTONS['delete_good_confirm'][language_code],
                                  reply_markup=il.deletion_confirmation_good(good_id,
                                                                             language_code))


@admin.callback_query(Admin(), F.data.startswith('back_to_good'))
async def back_to_good(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = int(callback.data.split("_")[-1])
    good_data = await get_good(good_id)
    await callback.message.answer_photo(caption=f"${good_data[2]}\n\n{good_data[0]}\n\n{good_data[1]}",
                                        photo=good_data[3],
                                        reply_markup=il.manage_good(good_id, language_code))


@admin.callback_query(Admin(), F.data.startswith("confirmed_delete_good_"))
async def confirmed_delete_good(callback: CallbackQuery):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = int(callback.data.split("_")[-1])
    await callback.message.delete()
    await callback.message.answer(REPLY_BUTTONS['deleted'][language_code],
                                  reply_markup=await il.category_management(language_code, good_id))
    await delete_good(good_id)


@admin.callback_query(Admin(), F.data.startswith('change_desc_'))
async def good_change_description(callback: CallbackQuery, state: FSMContext):
    good_id = callback.data.split("_")[-1]
    language_code = await get_user_language(callback.message.chat.id)
    await state.set_state(AlterGoodDescription.id)
    await state.update_data(id=int(good_id))
    await state.set_state(AlterGoodDescription.description)
    await callback.message.answer(ADMIN_PANEL['good_desc'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AlterGoodDescription.description)
async def insert_new_description(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        await state.update_data(description=message.text)
        data = await state.get_data()
        await change_good_description(data['description'], data['id'])
        good_data = await get_good(data['id'])
        await message.answer_photo(caption=f"${good_data[2]}\n\n{good_data[0]}\n\n{good_data[1]}", photo=good_data[3],
                                   reply_markup=il.manage_good(data['id'], language_code))
        await state.clear()
        await message.answer(ADMIN_PANEL['success'][language_code],
                                      reply_markup=rp.admins_panel(language_code))


@admin.callback_query(Admin(), F.data.startswith("change_photo_"))
async def good_change_photo(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = callback.data.split("_")[-1]
    await state.set_state(AlterGoodPhoto.id)
    await state.update_data(id=int(good_id))
    await state.set_state(AlterGoodPhoto.photo)
    await callback.message.answer(ADMIN_PANEL['good_photo'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AlterGoodPhoto.photo, ~F.photo)
async def add_photo_incorrect(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        await message.answer(ADMIN_PANEL['not_photo'][language_code])


@admin.message(Admin(), AlterGoodPhoto.photo, F.photo)
async def insert_good_photo(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        await state.update_data(photo=message.photo[-1].file_id)
        data = await state.get_data()
        await change_good_photo(data['photo'], data['id'])
        good_data = await get_good(data['id'])
        await message.answer_photo(caption=f"${good_data[2]}\n\n{good_data[0]}\n\n{good_data[1]}", photo=good_data[3],
                                   reply_markup=il.manage_good(data['id'], language_code))
        await state.clear()
        await message.answer(ADMIN_PANEL['success'][language_code],
                                      reply_markup=rp.admins_panel(language_code))


@admin.callback_query(Admin(), F.data.startswith("change_category_"))
async def good_change_category(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = callback.data.split("_")[-1]
    await state.set_state(AlterGoodCategory.id)
    await state.update_data(id=int(good_id))
    await state.set_state(AlterGoodCategory.category)
    await callback.message.answer(ADMIN_PANEL['good_category'][language_code],
                                  reply_markup=await il.categories_selection(language_code))


@admin.callback_query(Admin(), AlterGoodCategory.category)
async def insert_good_category(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    if callback.data == 'cancelled_action':
        await state.clear()
        await callback.message.answer(MESSAGES["cancelled_message"][language_code],
                                      reply_markup=rp.admins_panel(language_code))
    else:
        category = int(callback.data.split('_')[1])
        await state.update_data(category=category)
        data = await state.get_data()
        await change_good_category(data['category'], data['id'])
        good_data = await get_good(data['id'])
        await callback.message.answer_photo(caption=f"${good_data[2]}\n\n{good_data[0]}\n\n{good_data[1]}",
                                            photo=good_data[3],
                                            reply_markup=il.manage_good(data['id'], language_code))
        await state.clear()
        await callback.message.answer(ADMIN_PANEL['success'][language_code],
                                      reply_markup=rp.admins_panel(language_code))


@admin.callback_query(Admin(), F.data.startswith("change_price_"))
async def good_change_price(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    good_id = callback.data.split("_")[-1]
    await state.set_state(AlterGoodPrice.id)
    await state.update_data(id=int(good_id))
    await state.set_state(AlterGoodPrice.price)
    await callback.message.answer(ADMIN_PANEL['good_cost'][language_code], reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AlterGoodPrice.price)
async def insert_good_price(message: Message, state: FSMContext):
    language_code = await get_user_language(message.chat.id)
    if message.text.isdigit():
        await state.update_data(price=int(message.text))
        data = await state.get_data()
        await change_good_price(data['price'], data['id'])
        good_data = await get_good(data['id'])
        await message.answer_photo(caption=f"${good_data[2]}\n\n{good_data[0]}\n\n{good_data[1]}", photo=good_data[3],
                                   reply_markup=il.manage_good(data['id'], language_code))
        await state.clear()
        await message.answer(ADMIN_PANEL['success'][language_code],
                             reply_markup=rp.admins_panel(language_code))
    elif message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                                      reply_markup=rp.admins_panel(language_code))
    else:
        await message.answer(ADMIN_PANEL['not_digit_price'][language_code])


@admin.callback_query(Admin(), F.data.startswith("answer_to_"))
async def bug_report(callback: CallbackQuery, state: FSMContext):
    language_code = await get_user_language(callback.message.chat.id)
    receiver = int(callback.data.split("_")[2])
    await state.set_state(AnswerMessage.to)
    await state.update_data(to=receiver)
    await state.set_state(AnswerMessage.message)
    await callback.message.answer(MESSAGES['message_wait'][language_code],
                                  reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AnswerMessage.message)
async def send_newsletter(message: Message, state: FSMContext, bot: Bot) -> None:
    language = await get_user_language(message.chat.id)
    data = await state.get_data()
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language],
                                      reply_markup=rp.admins_panel(language))
    else:
        try:
            await bot.send_message(chat_id=data['to'], text=f"<b>{MESSAGES['message_answered'][language]}</b>")
            await message.send_copy(chat_id=data['to'])
        except:
            await message.answer(ADMIN_BUTTONS['feedback_error'][language], reply_markup=rp.admins_panel(language))
        await message.answer(MESSAGES['message_sent'][language], reply_markup=rp.admins_panel(language))
        await state.clear()


@admin.callback_query(Admin(), F.data.startswith("alter_category_"))
async def alter_category_handler(callback: CallbackQuery, state: FSMContext):
    category_id = int(callback.data.split('_')[-1])
    language_code = await get_user_language(callback.message.chat.id)
    await state.set_state(AlterCategory.id)
    await state.update_data(id=category_id)
    await state.set_state(AlterCategory.title_eng)
    await callback.message.answer(ADMIN_PANEL['category_add_eng'][language_code],
                                  reply_markup=rp.cancel_operation(language_code))


@admin.message(Admin(), AlterCategory.title_eng)
async def add_category_eng(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    if message.text in list(MESSAGES['cancelled_action'].values()):
        await state.clear()
        await message.answer(MESSAGES["cancelled_message"][language_code],
                             reply_markup=rp.admins_panel(language_code))
    else:
        await state.update_data(title_eng=message.text)
        await state.set_state(AlterCategory.title_uzb)
        await message.answer(ADMIN_PANEL['category_add_uzb'][language_code])


@admin.message(Admin(), AlterCategory.title_uzb)
async def add_category_uzb(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.update_data(title_uzb=message.text)
    await state.set_state(AlterCategory.title_rus)
    await message.answer(ADMIN_PANEL['category_add_rus'][language_code])


@admin.message(Admin(), AlterCategory.title_rus)
async def add_category_rus(message: Message, state: FSMContext) -> None:
    language_code = await get_user_language(message.chat.id)
    await state.update_data(title_rus=message.text)
    data = await state.get_data()
    await alter_category(data['id'], data['title_eng'], data['title_uzb'], data['title_rus'])
    await message.answer(ADMIN_PANEL['success'][language_code], reply_markup=await il.for_admins_categories_kb(language_code))
    await state.clear()