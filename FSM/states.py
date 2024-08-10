from aiogram.filters.state import State, StatesGroup


class AddAdminStaff(StatesGroup):
    telegram_id = State()
    name = State()


class AddCategory(StatesGroup):
    title_eng = State()
    title_rus = State()
    title_uzb = State()


class AlterCategory(StatesGroup):
    id = State()
    title_eng = State()
    title_rus = State()
    title_uzb = State()


class AddGoods(StatesGroup):
    title = State()
    photo = State()
    description = State()
    category = State()
    price = State()


class Feedback(StatesGroup):
    message = State()


class UserRegistration(StatesGroup):
    full_name = State()
    contact = State()


class NewsLetter(StatesGroup):
    message = State()


class EngDescription(StatesGroup):
    message = State()


class RusDescription(StatesGroup):
    message = State()


class UzbDescription(StatesGroup):
    message = State()


class ContactsEdit(StatesGroup):
    message = State()


class AlterGoodTitle(StatesGroup):
    id = State()
    title = State()


class AlterGoodDescription(StatesGroup):
    id = State()
    description = State()


class AlterGoodPhoto(StatesGroup):
    id = State()
    photo = State()


class AlterGoodCategory(StatesGroup):
    id = State()
    category = State()


class AlterGoodPrice(StatesGroup):
    id = State()
    price = State()


class AnswerMessage(StatesGroup):
    to = State()
    message = State()
