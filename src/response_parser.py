import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ResponseParser:
    @staticmethod
    def parse_to_json_format(data, exclude_unknown):
        parsed_data = []
        for item in data:
            parsed_item = {
                "email": item.get("email"),
                "password": item.get("password"),
                "source": item.get("source", {}),
                "fields": item.get("fields", [])
            }
            if exclude_unknown:
                parsed_item["source"] = {k: v for k, v in parsed_item["source"].items() if v is not None and v != "Unknown"}
            if "breach_date" in parsed_item["source"]:
                parsed_item["source"]["breach_date"] = ResponseParser.format_date(parsed_item["source"]["breach_date"])
            parsed_data.append(parsed_item)
        return json.dumps(parsed_data, indent=4)

    @staticmethod
    def parse_to_combolist_format(data):
        combolist = []
        for item in data:
            username = item.get('username', 'Unknown')
            password = item.get('password', 'Unknown')
            email = item.get('email', None)
            ip = item.get('ip', None)
            website = item.get('source', {}).get('name', None)
            breach_date = item.get('source', {}).get('breach_date', None)
            if breach_date:
                breach_date = ResponseParser.format_date(breach_date)
            
            entry = f"{username}:{password}"
            if website:
                entry += f" Website: {website}"
                if breach_date and breach_date != 'Unknown Date':
                    entry += f" ({breach_date})"
            if email and email != 'Unknown':
                entry += f" Email: {email}"
            if ip and ip != 'Unknown':
                entry += f" IP: {ip}"
            
            combolist.append(entry)

        return '\n'.join(combolist)

    @staticmethod
    def parse_to_csv_format(data):
        csv_data = []
        for item in data:
            username = item.get('username', 'Unknown')
            password = item.get('password', 'Unknown')
            email = item.get('email', None) if 'email' in item.get('fields', []) else 'Unknown'
            ip = item.get('ip', None) if 'ip' in item.get('fields', []) else 'Unknown'
            website = item.get('source', {}).get('name', 'Unknown')
            breach_date = item.get('source', {}).get('breach_date', 'Unknown')
            if breach_date != 'Unknown':
                breach_date = ResponseParser.format_date(breach_date)

            row = {
                'Username': username,
                'Password': password,
                'Email': email if email != 'Unknown' else '',
                'IP': ip if ip != 'Unknown' else '',
                'Website': website,
                'Breach Date': breach_date
            }
            csv_data.append(row)
        return csv_data

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
        
    @staticmethod
    def process_output(data, format, settings):
        if format == 'json':
            return ResponseParser.parse_to_json_format(data, settings.get('exclude_unknown', True))
        elif format == 'csv':
            return ResponseParser.parse_to_csv_format(data)
        elif format == 'combolist':
            return ResponseParser.parse_to_combolist_format(data)
        else:
            raise ValueError("Unsupported format specified")
