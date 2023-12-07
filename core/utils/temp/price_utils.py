DISCOUNT_90_DAYS = 10
DISCOUNT_180_DAYS = 15
DISCOUNT_360_DAYS = 25


async def calculate_booking_price(price_per_day, days):
    price = price_per_day * days

    if 90 <= days < 180:
        price = ((price_per_day * days) / 100.0) * (100.0 - DISCOUNT_90_DAYS)
    elif 180 <= days > 360:
        price = ((price_per_day * days) / 100.0) * (100.0 - DISCOUNT_180_DAYS)
    elif 360 <= days:
        price = ((price_per_day * days) / 100.0) * (100.0 - DISCOUNT_360_DAYS)

    return price


async def calculate_total_order_price(bookings):
    total_price = 0.0
    for booking in bookings:
        total_price += booking.price

    return total_price

