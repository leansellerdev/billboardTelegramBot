from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.state import State, StatesGroup
from redis.asyncio.client import Redis


redis: Redis = Redis(host='localhost', port=6379)
storage: RedisStorage = RedisStorage(redis=redis)


class FSMStart(StatesGroup):
    start = State()
    self_orders = State()
    billboards = State()
    about = State()


class FSMRegistration(StatesGroup):

    name = State()
    surname = State()
    email = State()
    phone_number = State()
    end = State()


class FSMChangeData(StatesGroup):

    change_phone = State()
    change_email = State()
