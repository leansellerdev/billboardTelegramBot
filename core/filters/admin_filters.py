from aiogram.filters import Filter
from aiogram.types import Message
from core.utils.users_utils import user_registered


class UserIDFilter(Filter):

    async def __call__(self, message: Message):
        return await user_registered(message.text)
