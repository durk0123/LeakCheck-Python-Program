
# LeakCheck Python Program
## THIS TOOL HAS BEEN UPDATED TO THE NEWEST LEAKCHECK API 

## Introduction
This repository contains a Python-based tool designed to interact with the LeakCheck API. LeakCheck is a powerful API that allows users to check for data leaks and breaches. This program is built to provide an easy-to-use interface to access the capabilities of the LeakCheck API, including checking for leaks, parsing responses, and handling errors.

**NOTE: THIS PYTHON PROJECT IS ONLY FOR THE PAID VERSION OF LEAKCHECK ONLY**

## Features
- **LeakCheck API Integration:** Seamlessly integrates with the LeakCheck API.
- **Error Handling:** Robust error handling for reliable operations.
- **Response Parsing:** Efficiently parses API responses for ease of use.
- **Utility Functions:** Additional utilities to enhance the functionality.
- **Automatic Folder Creation:** Automatically creates `queries` and `config` folders for searches and configurations.
- **Formatted Output:** Human-readable response sizes and detailed time taken for queries.

## Installation
To use this program, clone this repository and install the required dependencies.

```bash
git clone https://github.com/durk0123/leakcheck-python.git
cd leakcheck-python
pip install -r requirements.txt
```

## Configuration
Before running the program, ensure you have your API key in the `config/config.json` file. You can obtain your API key from the LeakCheck account settings.

Available types of output formats:
`csv`, `json`, `combolist`

### Sample `config.json`:
```json
{
    "api_key": "YOUR_API_KEY",
    "logging_enabled": true,
    "settings": {
        "output_format": "json",
        "exclude_unknown": true,
        "save_raw_json_response": true,
        "rate_limit_retry_seconds": 60
    }
}
```

## Usage
To use this tool, simply run the `leakcheck.py` file.

```bash
python leakcheck.py
```

Follow the prompts to enter the type of data to check and the specific data value.

## API Reference
For detailed information about the LeakCheck API, visit the [LeakCheck API Documentation](https://wiki.leakcheck.io/en/api/api-v2-pro).

### Key Points:
- **Authorization:** Pass your API key in the `X-API-Key` header.
- **Sample Query:**
    ```plaintext
    GET https://leakcheck.io/api/v2/query/example@example.com
    ```
- **Response:**
    ```json
    {
        "success": true,
        "found": 1,
        "quota": 400,
        "result": [...]
    }
    ```

- **Errors:**
  - Missing X-API-Key header: 401
  - Invalid X-API-Key: 400
  - Too many requests: 429

- **Limits:**
  - Default limit of 3 requests per second for the Pro API.

## Contributing
This project is not being actively maintained, but contributions are welcome. Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
