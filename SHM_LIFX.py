#SHM_LIFX.py
import requests
from config import LIFX_TOKEN
import time

# Global variables for API access
BASE_URL = "https://api.lifx.com/v1/lights"
HEADERS = {"Authorization": f"Bearer {LIFX_TOKEN}"}

def send_feedback(message):
    """
    Placeholder for sending feedback, to be integrated with TTS.
    """
    print(message)  # This should be replaced with a call to the TTS module

def perform_request(url, method="put", payload=None):
    """
    Performs an HTTP request and handles errors with user-friendly feedback.
    """
    try:
        response = requests.request(method, url, headers=HEADERS, json=payload)
        if response.status_code in [200, 207]:
            return response.json()
        else:
            send_feedback("Oh snap! Something went wrong with the lights. Let me check that.")
            return None
    except Exception as e:
        send_feedback("Whoops! Tripped on some wires. Give me a sec to sort this out.")
        return None

def set_light_state(selector, power=None, brightness=None, color=None, kelvin=None):
    """
    Attempts to set the state of a LIFX light, including power, brightness, color, and Kelvin,
    up to 100 times in under a minute before reporting failure.
    """
    url = f"{BASE_URL}/{selector}/state"
    payload = {}
    if power:
        payload["power"] = power
    if brightness:
        payload["brightness"] = brightness
    if color:
        payload["color"] = color
    if kelvin:
        payload["color"] = f"kelvin:{kelvin}"
    
    max_attempts = 100
    attempt = 0
    success = False
    
    while attempt < max_attempts and not success:
        response = perform_request(url, payload=payload)
        if response:
            # Assuming response contains a list of affected lights for simplicity
            affected_lights = [light['label'] for light in response] if response else ['the light']
            affected_lights_str = ", ".join(affected_lights)
            feedback_msg = f"Alrighty, I've adjusted {affected_lights_str} for you! ✨"
            if color or kelvin:
                feedback_msg += f" Set to {'colorful shades' if color else 'a chill temperature'}."
            send_feedback(feedback_msg)
            success = True
        else:
            time.sleep(0.6)  # Sleep to spread out the requests and avoid hitting the rate limit
            attempt += 1
    
    if not success:
        send_feedback("Hmm, seems like I couldn't chat with the lights after trying a bunch. Let me try that again later.")

def handle_lifx_command(command_text):
    command_text = command_text.lower()
    selector = "label:Desk Light"  # Targeting your 'Desk Light'

    # Checking for power commands
    if "turn on the light" in command_text or "turn on the desk light" in command_text:
        set_light_state(selector, power="on")
    elif "turn off the light" in command_text or "turn off the desk light" in command_text:
        set_light_state(selector, power="off")
    
    # Checking for color commands
    elif "set light to blue" in command_text or "set desk light to blue" in command_text:
        set_light_state(selector, color="blue")
    elif "set light to red" in command_text or "set desk light to red" in command_text:
        set_light_state(selector, color="red")
    
    # Checking for brightness commands
    elif "dim the light" in command_text or "dim the desk light" in command_text:
        set_light_state(selector, brightness=0.2)  # Example: dim to 20% brightness
    elif "brighten the light" in command_text or "brighten the desk light" in command_text:
        set_light_state(selector, brightness=1)  # Brighten to 100% brightness
    
    # Add more conditions as needed for other functionalities
    else:
        send_feedback("I'm not sure how to do that with the light. Can you try a different command?")