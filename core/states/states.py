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


class FSMSelfOrders(StatesGroup):
    orders = State()
    change_order = State()
    get_orders = State()
    update_billboard = State()
    order_id = State()
    billboard_id = State()
    booking_id = State()
    start_date = State()
    new_date_end = State()
    data_changed_end = State()
    old_price = State()
    new_price = State()


class FSMMakeOrder(StatesGroup):
    client_id = State()
    manager_id = State()
    total_price = State()
    created_date = State()
    created_date_y = State()
    created_date_m = State()
    created_date_d = State()
    created_date_h = State()
    created_date_min = State()
    created_date_s = State()
    created_date_ms = State()

    order_id = State()
    billboard_id = State()
    price = State()

    start_date = State()
    start_date_y = State()
    start_date_m = State()
    start_date_d = State()

    end_date = State()
    end_date_y = State()
    end_date_m = State()
    end_date_d = State()

    choose_billboard = State()
    start_order = State()
    complete_order = State()
    cancel_order = State()
    final_complete_order = State()

    free_period = State()
    not_free_period = State()
    is_continue = State()


class FSMRegistration(StatesGroup):

    name = State()
    surname = State()
    email = State()
    phone_number = State()
    manager_id = State()
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
