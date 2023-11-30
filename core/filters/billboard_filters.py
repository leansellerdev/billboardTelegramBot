from aiogram.filters import Filter
from aiogram.types import Message

from core.utils.billboard_utils import billboard_exists


class BillboardExistsFilter(Filter):

    async def __call__(self, message: Message):
        return await billboard_exists(message.text.title())