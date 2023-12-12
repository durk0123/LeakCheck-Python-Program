import json
import os
import sys
import logging
import requests
import platform
from src.leakcheck_api import LeakCheckApi
from src.utils import validate_input, is_valid_data_type
from src.response_parser import ResponseParser

CONFIG_PATH = 'config/config.json'
DEFAULT_CONFIG = {
    "api_key": "YOUR_API_KEY",
    "logging_enabled": True,
    "default_output_format": "json",
    "rate_limit_retry_seconds": 60
}

def ensure_config_exists():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)

def load_config():
    with open(CONFIG_PATH, 'r') as file:
        return json.load(file)

def setup_logging(enabled):
    if enabled:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)

def validate_api_key(api_key):
    test_url = "https://leakcheck.io/api"
    test_params = {
        'key': api_key,
        'check': 'test@example.com',
        'type': 'email'
    }
    try:
        response = requests.get(test_url, params=test_params)
        if response.status_code == 200:
            data = response.json()
            return data.get('success', False)
        return False
    except requests.RequestException:
        return False
    
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def main():
    clear_console()
    ensure_config_exists()
    config = load_config()
    setup_logging(config.get('logging_enabled', False))

    api_key = config.get('api_key', 'YOUR_API_KEY')
    if not validate_api_key(api_key):
        api_key = input("Please enter your API key: ").strip()
        if not validate_api_key(api_key):
            logging.error("Invalid API key. Exiting.")
            sys.exit(1)
        else:
            config['api_key'] = api_key
            with open(CONFIG_PATH, 'w') as file:
                json.dump(config, file, indent=4)

    api = LeakCheckApi(api_key, config.get('rate_limit_retry_seconds', 60))

    data_type = input("Enter the type of data to check (email, username, etc.): ").strip().lower()
    
    if data_type == "username":
        data_type = "login"

    if not is_valid_data_type(data_type):
        logging.error(f"Invalid data type: {data_type}")
        sys.exit(1)

    data_value = input(f"Enter the {data_type} to check: ").strip()
    if not validate_input(data_type, data_value):
        logging.error(f"Invalid {data_type} format.")
        sys.exit(1)

    response = api.get_data(data_type, data_value)
    if response and response.get('success'):
        format_choice = config.get('default_output_format', 'json')
        output = ''
        if format_choice == 'json':
            output = ResponseParser.parse_to_json_format(response.get('result', []))
        elif format_choice == 'combolist':
            output = ResponseParser.parse_to_combolist_format(response.get('result', []))
        else:
            logging.error("Invalid format choice. Exiting.")
            return

        query_folder = "queries"
        os.makedirs(query_folder, exist_ok=True)
        file_extension = 'json' if format_choice == 'json' else 'txt'
        file_name = f"{query_folder}/{data_type}_{data_value}.{file_extension}"
        with open(file_name, 'w') as file:
            file.write(output)

        amount_of_results = len(response.get('result', []))
        print(f"\n> Data saved in: {file_name} | {amount_of_results} Results")
    else:
        print("No results found or an error occurred.")

if __name__ == "__main__":
    main()