import re
import phonenumbers

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


async def email_valid(email: str):

    if not re.fullmatch(email_regex, email):
        return False

    return True


async def phone_valid(phone_number: str):

    try:
        phone = phonenumbers.parse(phone_number)
    except:
        return False

    return phonenumbers.is_valid_number(phone)
