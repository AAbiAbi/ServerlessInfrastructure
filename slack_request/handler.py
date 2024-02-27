import json
import requests
# categorize the input into one of the specified types: a name inquiry, a current time/date inquiry, or a request for figlet generation.
def handle(req):
    """Identify the type of user request from the input question."""
    # Normalize and analyze the request
    req_lower = req.lower().strip()
    response_type = "unknown"  # Default response type
    
    # Determine the type of question
    
    if "current time" in req_lower or "date" in req_lower or "time" in req_lower:
        response_type = "time"
    elif req_lower.startswith("generate a figlet for"):
        response_type = "figlet"
    elif "name" in req_lower:
        response_type = "name"
    
    # Construct a response with the request type
    response = {"request_type": response_type, "original_request": req}
    # return json.dumps(response)
    
    # Categorize the request and prepare the payload
    payload = json.dumps(response)
    
    # Make the HTTP POST request to slack-interactive
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post("http://gateway:8080/function/slack-interactive", data=payload, headers=headers)
    # # URL for the slack-interactive function
    # slack-interactive
    # # Return the response from slack-interactive
    # return response.text
        if response.status_code == 200:
                # Return the response from slack-interactive
                return response.text
        else:
            # Handle unexpected status code
            return f"Error: Received status code {response.status_code} from slack-interactive"
    except requests.exceptions.RequestException as e:
        # Handle request to slack-interactive failing
        return f"Error: Failed to send request to slack-interactive. Exception: {str(e)}"

    
# This function now returns a JSON object with the category of the request and the original request text.