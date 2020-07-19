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
    # post_data = {
    #     **post_data,
    #     'api_key': settings.GATEWAY_API_KEY,
    #     'time_stamp': str(int(timestamp)),
    #     'hotel_id': settings.GATEWAY_HOTEL_ID,
    #     'language_id': GATEWAY_LANGUAGE_ID
    # }
    # check_sum = settings.GATEWAY_API_HASH + "_" + json.dumps(post_data) + "_" + str(int(timestamp))
    # json_data = {
    #     'data': json.dumps(post_data),
    #     'check_sum': hashlib.md5(s.encode('utf-8')).hexdigest()
    # }
    json_data = post_data
    headers = {'X-API-KEY': settings.GATEWAY_API_KEY}
    try:
        response = requests.post(settings.GATEWAY_API_HOST + url, timeout=360, json=post_data, headers=headers, verify=False)
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