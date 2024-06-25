import re

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_username(username):
    return len(username) >= 2

def validate_phone(phone):
    return len(phone) >= 5 and phone.isdigit()

def validate_domain(domain):
    return re.match(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$", domain)

def validate_auto(auto):
    return len(auto) >= 1

def is_valid_data_type(data_type):
    valid_data_types = ['email', 'login', 'phone', 'domain', 'keyword', 'hash', 'auto'] # 'mc' removed due to being removed in API
    return data_type in valid_data_types

def validate_input(data_type, data_value):
    validators = {
        'email': validate_email,
        'login': validate_username,
        'phone': validate_phone,
        'domain': validate_domain,
        'auto': validate_auto
    }

    validator = validators.get(data_type)
    return validator(data_value) if validator else False

class CustomColors:
    PURPLE = '\033[38;2;84;71;247m'
    BLUE = '\033[38;2;61;186;240m'
    GREEN = '\033[38;2;144;238;144m'
    RED = '\033[38;2;255;99;71m'
    RESET = '\033[0m'
