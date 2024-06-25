import json
import os
import sys
import logging
import requests
import platform
import time
import csv
import math
from src.leakcheck_api import LeakCheckApi
from src.utils import validate_input, is_valid_data_type, CustomColors
from src.response_parser import ResponseParser
from colorama import init
from getpass4 import getpass

# Initialize colorama
init(autoreset=True)

CONFIG_PATH = 'config/config.json'
DEFAULT_CONFIG = {
    "api_key": "YOUR_API_KEY",
    "logging_enabled": True,
    "settings": {
        "output_format": "json",
        "exclude_unknown": False,
        "save_raw_json_response": False,
        "rate_limit_retry_seconds": 60
    }
}

def print_status(message, status):
    color = CustomColors.GREEN if status else CustomColors.RED
    status_char = "✓" if status else "✗"
    print(f"{color}{status_char}{CustomColors.RESET} {message}")

def ensure_config_exists():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    if not os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as file:
            json.dump(DEFAULT_CONFIG, file, indent=4)
        print_status("Added config file", True)

def load_config():
    with open(CONFIG_PATH, 'r') as file:
        return json.load(file)

def setup_logging(enabled):
    if enabled:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)

def clear():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def validate_server():
    test_url = "https://leakcheck.io/api"
    try:
        response = requests.get(test_url)
        return response.status_code != 502
    except requests.RequestException as e:
        logging.error(f"RequestException: {e}")
        return False

def validate_api_key(api_key):
    test_url = "https://leakcheck.io/api/v2/query/test@example.com"
    headers = {'X-API-Key': api_key}
    try:
        response = requests.get(test_url, headers=headers)
        if response.status_code == 200:
            return True
        elif response.status_code == 502:
            print_status("API Server went down when validating API Key", False)
            sys.exit(1)
        elif response.status_code in [401, 400, 403, 422]:
            logging.error(f"API key validation failed with status code {response.status_code}")
            return False
        else:
            logging.error(f"Unexpected status code {response.status_code} during API key validation")
            return False
    except requests.RequestException as e:
        logging.error(f"RequestException: {e}")
        return False

def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def main():
    clear()
    print(f"{CustomColors.PURPLE}Leak{CustomColors.BLUE}Check{CustomColors.RESET}\n")

    ensure_config_exists()
    config = load_config()
    settings = config.get('settings', {})
    setup_logging(config.get('logging_enabled', False))

    if validate_server():
        print_status("API Status: API server is up", True)
    else:
        print_status("API Status: API server is down [502 Bad Gateway]", False)
        sys.exit(1)

    api_key = config.get('api_key', 'YOUR_API_KEY')
    attempts = 0
    while attempts < 3:
        if api_key != 'YOUR_API_KEY' and validate_api_key(api_key):
            config['api_key'] = api_key
            with open(CONFIG_PATH, 'w') as file:
                json.dump(config, file, indent=4)
            break
        else:
            print_status("API Key Status: Missing or invalid API Key", False)
            api_key = getpass(f"{CustomColors.GREEN}➜{CustomColors.RESET} Enter API Key: ")
            attempts += 1

    if not validate_api_key(api_key):
        print_status("API Key Status: Missing or invalid API Key", False)
        sys.exit(1)

    clear()
    print(f"{CustomColors.PURPLE}Leak{CustomColors.BLUE}Check{CustomColors.RESET}\n")
    print_status("API Status: API server is up", True)
    masked_api_key = api_key[:15] + '*' * (len(api_key) - 20)
    print_status(f"Validated API Key from config: {masked_api_key}", True)
    time.sleep(0.5)
    print_status(f"Output format configured as: {settings['output_format']}", True)
    time.sleep(0.5)
    save_raw_json_status = settings.get('save_raw_json_response', False)
    print_status("Save Raw JSON response", save_raw_json_status)
    time.sleep(0.5)
    exclude_unknown_status = settings.get('exclude_unknown', False)
    print_status("Exclude Unknown", exclude_unknown_status)
    time.sleep(1.3)

    api = LeakCheckApi(api_key, settings.get('rate_limit_retry_seconds', 60))

    clear()
    print(f"{CustomColors.PURPLE}Leak{CustomColors.BLUE}Check{CustomColors.RESET}\n")
    data_type = input(f"[{CustomColors.PURPLE}Leak{CustomColors.BLUE}Check{CustomColors.RESET}] Enter the type of data to check (email, username, etc.): ").strip().lower()
    
    if data_type == "username":
        data_type = "login"

    if not is_valid_data_type(data_type):
        print_status(f"Invalid data type: {data_type}", False)
        sys.exit(1)

    data_value = input(f"[{CustomColors.PURPLE}Leak{CustomColors.BLUE}Check{CustomColors.RESET}] Enter the {data_type} to check: ").strip()
    print()

    if not validate_input(data_type, data_value):
        print_status(f"Invalid {data_type} format.", False)
        sys.exit(1)

    start_time = time.time()

    try:
        response = api.get_data(data_type, data_value)
        if response and response.get('success'):
            if response.get('found', 0) == 0:
                print_status("No results found.", False)
                elapsed_time = time.time() - start_time
                print_status(f"Time taken: {elapsed_time:.2f} seconds", True)
            else:
                output_format = settings.get('output_format', 'json')
                output = ResponseParser.process_output(response.get('result', []), output_format, settings)

                query_folder = "queries"
                os.makedirs(query_folder, exist_ok=True)
                file_extension = 'csv' if output_format == 'csv' else 'json' if output_format == 'json' else 'txt'
                file_name = f"{query_folder}/{data_type}_{data_value}.{file_extension}"

                if settings.get('save_raw_json_response', False):
                    raw_file_name = f"{query_folder}/{data_type}_{data_value}_raw.json"
                    with open(raw_file_name, 'w') as raw_file:
                        json.dump(response, raw_file, indent=4)
                    print_status(f"Raw JSON response saved in: {raw_file_name}", True)

                if output_format == 'csv':
                    with open(file_name, mode='w', newline='') as file:
                        fieldnames = output[0].keys() if output else []
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(output)
                else:
                    with open(file_name, 'w') as file:
                        file.write(output)

                print_status(f"Data saved in: {file_name}", True)
                response_size = len(json.dumps(response))
                formatted_size = format_size(response_size)
                print_status(f"Size: {formatted_size}", True)
                elapsed_time = time.time() - start_time
                print_status(f"Time taken: {elapsed_time:.2f} seconds", True)
        else:
            print_status("An error occurred.", False)
            print(f"Error details: {response}")
            elapsed_time = time.time() - start_time
            print_status(f"Time taken: {elapsed_time:.2f} seconds", False)
    except requests.RequestException as e:
        logging.error(f"RequestException during data query: {e}")
        print_status("An error occurred during the request. Please try again later.", False)
        elapsed_time = time.time() - start_time
        print_status(f"Time taken: {elapsed_time:.2f} seconds", False)

if __name__ == "__main__":
    main()
