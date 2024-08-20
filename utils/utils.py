from aiogram.filters import Filter
from aiogram.types import Message

from database.queries import *

import re

from dotenv import dotenv_values
import os

dotenv = dotenv_values(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

SYSTEM_ADMINS = [int(dotenv['ADMIN_1_ID']), int(dotenv['ADMIN_2_ID']), int(dotenv['DEV_ID'])]


class Admin(Filter):
    async def __call__(self, message: Message) -> bool:
        admins = SYSTEM_ADMINS + await get_admin_id()
        return message.from_user.id in admins


class MainAdmin(Filter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in SYSTEM_ADMINS


class Managers(Filter):
    async def __call__(self, message: Message) -> bool:
        workers = await get_admin_name()
        return message.from_user.id in SYSTEM_ADMINS and message.text in workers


def validate_phone_number(message):
    pattern = re.compile(r'^\+?\d[\d\s]{6,16}\d$')
    return bool(pattern.match(message))