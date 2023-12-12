import re

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_username(username):
    return len(username) >= 2

def validate_phone(phone):
    return len(phone) >= 5 and phone.isdigit()

def validate_minecraft_username(mc_username):
    return 3 <= len(mc_username) <= 16

def validate_domain(domain):
    return re.match(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$", domain)

def is_valid_data_type(data_type):
    valid_data_types = ['email', 'login', 'phone', 'mc', 'domain']
    return data_type in valid_data_types

def validate_input(data_type, data_value):
    validators = {
        'email': validate_email,
        'login': validate_username,
        'phone': validate_phone,
        'mc': validate_minecraft_username,
        'domain': validate_domain
    }

    validator = validators.get(data_type)
    return validator(data_value) if validator else False