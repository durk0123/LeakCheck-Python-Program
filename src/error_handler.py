def handle_error(response):
    error_messages = {
        "Missing params (key, check, type)": "Required parameters are missing.",
        "Invalid type": "Invalid lookup type provided.",
        "API Key is wrong": "The provided API key is invalid.",
        "API Key is blocked": "The API key is blocked.",
        "No license on this key": "No valid license found for this API key.",
        "Your query contains invalid characters": "The query contains prohibited characters.",
        "Enter at least 3 characters to search": "The search query is too short.",
        "Invalid email": "Invalid email address provided.",
        "Invalid domain": "Invalid domain provided.",
        "Invalid query": "The search query is invalid.",
        "IP linking is required": "IP address linking is required.",
        "Limit reached": "You have exceeded your plan limits.",
        "Not found": "No results found.",
        "Too many requests, you have been ratelimited": "Rate limit exceeded. Please try again later."
    }

    error = response.get('error')
    print(error_messages.get(error, "An unknown error occurred."))