import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResponseParser:
    @staticmethod
    def parse_to_json_format(data):
        parsed_data = []
        for item in data:
            login = item.get('line', 'Unknown Login')
            database = ', '.join(item.get('sources', ['Unknown Source'])) if item.get('sources') else 'Unknown Source'
            date = ResponseParser.format_date(item.get('last_breach', 'Unknown Date'))
            parsed_data.append({
                "Login": login,
                "Database": database,
                "Date": date
            })
        return json.dumps(parsed_data, indent=4)

    @staticmethod
    def parse_to_combolist_format(data):
        return '\n'.join([item.get('line', '') for item in data])

    @staticmethod
    def format_date(date_str):
        if not date_str or date_str == 'Unknown Date':
            return 'Unknown Date'
        
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m")
            years_ago = relativedelta(datetime.now(), date_obj).years
            formatted_date = date_obj.strftime("%B %d, %Y")
            return f"{formatted_date} ({years_ago} years ago)"
        except ValueError:
            return 'Unknown Date'