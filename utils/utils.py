from aiogram.filters import Filter
from aiogram.types import Message

from database.queries import *
from dotenv import dotenv_values

from configs import ADMINS_ID, DEV_ID

import re


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        admins = ADMINS_ID + DEV_ID + await get_admin_id()
        return message.from_user.id in admins


class MainAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in ADMINS_ID + DEV_ID


class Managers(Filter):
    async def __call__(self, message: Message) -> bool:
        workers = await get_admin_name()
        return message.from_user.id in ADMINS_ID + DEV_ID and message.text in workers


def validate_phone_number(message):
    pattern = re.compile(r'^\+?\d[\d\s]{6,16}\d$')
    return bool(pattern.match(message))