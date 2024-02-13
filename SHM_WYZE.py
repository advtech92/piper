# SHM_WYZE.py (Smart Home Module - Wyze Support)
import os
import logging
import wyze_sdk
from config import WYZE_ACCESS_TOKEN
from wyze_sdk import Client
from wyze_sdk.errors import WyzeApiError

token = WYZE_ACCESS_TOKEN

client = Client(token)

try:
    response = client.devices_list()
    for device in client.devices_list():
        print(f"MAC Address: {device.mac}")
        print(f"Device Nickname: {device.nickname}")
        print(f"Is Online?: {device.is_online}")
        #print(f"Product Mode: {device.product_model}")
except WyzeApiError as e:
    print:(f"Encounted an error: {e}")