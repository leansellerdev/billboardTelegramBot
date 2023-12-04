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


class FSMMakeOrder(StatesGroup):

    choose_billboard = State()
    start_order = State()
    start_date = State()
    end_date = State()
    complete_order = State()


class FSMRegistration(StatesGroup):

    name = State()
    surname = State()
    email = State()
    phone_number = State()
    end = State()


class FSMChangeData(StatesGroup):

    change_phone = State()
    change_email = State()


class FSMAdminPanel(StatesGroup):

    start = State()
    get_users = State()
    personal_management = State()
    set_manager = State()
    get_managers = State()


class FSMManagerPanel(StatesGroup):

    start = State()
    my_clients = State()
    billboards = State()
    statistics = State()


class FSMBillboards(StatesGroup):

    billboard_name = State()
    choose_action = State()
    change_price = State()


class FSMCreateBillboard(StatesGroup):
    name = State()
    width = State()
    height = State()
    sides = State()
    surface = State()
    address = State()
    pricePerDay = State()
    end = State()
