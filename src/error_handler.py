def handle_error(response):
    error_messages = {
        "Missing X-API-Key header": "Required API key is missing.",
        "Invalid X-API-Key": "The provided API key is invalid.",
        "Invalid type": "Invalid lookup type provided.",
        "Invalid email": "Invalid email address provided.",
        "Invalid query": "The search query is invalid.",
        "Invalid domain": "Invalid domain provided.",
        "Too short query (< 3 characters)": "The search query is too short.",
        "Invalid characters in query": "The query contains prohibited characters.",
        "Too many requests": "Rate limit exceeded. Please try again later.",
        "Active plan required": "An active plan is required to perform this query.",
        "Limit reached": "You have exceeded your plan limits.",
        "Could not determine search type automatically": "Could not determine search type automatically."
    }

    error = response.get('error')
    print(error_messages.get(error, "An unknown error occurred."))
