# from models.device import DeviceModel
import functools
import os
# from hmac import compare_digest
from flask import request

API_KEY=os.environ["API_KEY"]
# for each device, we can assign a api
def is_valid(api_key):
    # device = DeviceModel.find_by_device_key(api_key)
    # if device and compare_digest(device.device_key, api_key):
    #     return True
    return api_key == API_KEY

def api_required(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        api_key = request.headers.get("X-Api-Key")
        if not api_key:
            return {"message": "Please provide an API key"}, 400
        # Check if API key is correct and valid
        if request.method == "POST" and is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "The provided API key is not valid"}, 403
    return decorator