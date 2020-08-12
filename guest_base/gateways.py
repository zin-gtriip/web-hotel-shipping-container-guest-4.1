import datetime
import requests
import json
import hashlib
from json                       import JSONDecodeError
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _

# backend gateway
def post(url, post_data):
    # timestamp = datetime.datetime.now().timestamp() * 1e3
    post_data = {
        **post_data,
        'api_key': settings.GATEWAY_API_KEY,
        # 'site_id': settings.GATEWAY_SITE_ID,
        # 'site_name': settings.GATEWAY_SITE_NAME,
    }
    try:
        response = requests.post(settings.GATEWAY_URL + url, timeout=360, json=post_data, verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Error connecting to server')}
    return json_response

# ocr scanning
def ocr(image_file, scan_type):
    url = 'https://ocr.gtriip.com/ocr/'+ scan_type
    files = {scan_type: open(image_file, 'rb')}
    data = {'api_key':'F16430020E414D3CBB9FACB3DA8071F5'}
    try:
        response = requests.post(url, files=files, data=data)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Error connecting to server')}
    return json_response
