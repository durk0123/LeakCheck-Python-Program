import requests
import time
import logging
from src.error_handler import handle_error

class LeakCheckApi:
    def __init__(self, api_key, rate_limit_retry_seconds):
        self.api_key = api_key
        self.base_url = "https://leakcheck.io/api"
        self.rate_limit_retry_seconds = rate_limit_retry_seconds

    def get_data(self, data_type, data_value):
        params = {
            'key': self.api_key,
            'check': data_value,
            'type': data_type
        }
        while True:
            try:
                response = requests.get(self.base_url, params=params)
                response.raise_for_status()
                data = response.json()
                if not data.get('success'):
                    handle_error(data)
                    return None
                return data
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit exceeded
                    logging.warning("Rate limit exceeded. Retrying after {} seconds...".format(self.rate_limit_retry_seconds))
                    time.sleep(self.rate_limit_retry_seconds)
                    continue
                else:
                    logging.error(f"An HTTP error occurred: {e}")
                    return None
            except requests.RequestException as e:
                logging.error(f"An error occurred: {e}")
                return None