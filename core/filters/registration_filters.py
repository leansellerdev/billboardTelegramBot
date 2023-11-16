from aiogram.filters import Filter
from aiogram.types import Message

from core.utils.filters_utils import email_valid, phone_valid


class EmailFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return await email_valid(message.text)


class PhoneFilter(Filter):

    async def __call__(self, message: Message) -> bool:
        return await phone_valid(message.text)
