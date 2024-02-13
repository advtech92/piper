#SHM_LIFX.py
import requests
from config import LIFX_TOKEN

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
    Sets the state of a LIFX light, including power, brightness, color, and Kelvin,
    and returns information about the light(s) adjusted.
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
    
    response = perform_request(url, payload=payload)
    if response:
        # Extract light details from the response. This is a placeholder; actual implementation depends on LIFX response.
        # Assuming response contains a list of affected lights.
        affected_lights = [light['label'] for light in response] if response else ['the light']
        affected_lights_str = ", ".join(affected_lights)
        
        feedback_msg = f"Alrighty, I've adjusted {affected_lights_str} for you! ✨"
        if color or kelvin:
            feedback_msg += f" Set to {'colorful shades' if color else 'a chill temperature'}."
        send_feedback(feedback_msg)
    else:
        send_feedback("Hmm, seems like I couldn't chat with the lights. Let me try that again later.")