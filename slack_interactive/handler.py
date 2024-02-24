import datetime
import json
import random
import subprocess
import requests
import sys
import json
import shlex

def handle(req):
    # print("Raw request:", req) #debugging
    try:
        data = json.loads(req)
    except json.JSONDecodeError as e:
        print("JSON decoding failed:", e)
        return "Failed to decode the request. Invalid JSON format."

    request_type = data.get("request_type")
    original_request = data.get("original_request", "")

    if request_type == "name":
        return handle_name_request()
    elif request_type == "time":
        return handle_time_request()
    elif request_type == "figlet":
        return handle_figlet_request(original_request)
        
    else:
        return "Sorry, I didn't understand that."

def handle_name_request():
    responses = [
        "My name is ChatBot.",
        "I'm called ChatBot.",
        "You can call me ChatBot."
    ]
    #randomly choose a response
    
    chosen_response = random.choice(responses)
    return chosen_response
    # return json.dumps({"response": responses})

def handle_time_request():
    now = datetime.datetime.now()
    responses = [
        f"Current time is {now.strftime('%H:%M:%S')}.",
        f"It's now {now.strftime('%Y-%m-%d %H:%M:%S')}.",
        f"The date today is {now.strftime('%Y-%m-%d')}."
    ]
    chosen_response = random.choice(responses)
    return chosen_response

def handle_figlet_request(original_request):
    message = original_request.replace("generate a figlet for", "").strip()
    # Directly return the response from invoke_figlet without wrapping in JSON
    # print(f"Handling figlet request for message: {message}")
    return invoke_figlet(message)

def invoke_figlet(text):
    # print(f"Invoking figlet with text:",text)  # Log to stderr
    
    # url = 'http://127.0.0.1:8080/function/figlet'
    headers = {'Content-Type': 'text/plain'}
    try:
        response = requests.post("http://gateway:8080/function/figlet", data=text, headers=headers)
        # print(f"Response from figlet function: {response.text}")
        
        # Check if the response's content type is plain text
        if response.status_code == 200 and response.headers.get('Content-Type') == 'text/plain':
            # print("Figlet response received.", file=sys.stderr)
            # print(response.text)
            return response.text
        else:
            print("Unexpected response type.", file=sys.stderr)
            return "Error: Unexpected response type from figlet function."
    except requests.exceptions.RequestException as e:
        error_message = f"Request to figlet function failed: {e}"
        print(error_message, file=sys.stderr)
        return error_message
