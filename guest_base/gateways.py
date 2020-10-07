import datetime
import requests
import json
import hashlib
from json                       import JSONDecodeError
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _


# backend gateway
def backend_post(url, post_data):
    post_data = {
        **post_data,
        'api_key': settings.BACKEND_API_KEY,
        'site_id': settings.BACKEND_SITE_ID,
        'site_name': settings.BACKEND_SITE_NAME,
    }
    try:
        response = requests.post(settings.BACKEND_URL + url, json=post_data, timeout=360, verify=False)
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


# AMP gateway
def amp(method, url, **kwargs):
    headers = {'x-api-key': settings.AMP_API_KEY}
    try:
        if method == 'GET':
            response = requests.get(settings.AMP_URL + url, json=kwargs, headers=headers, timeout=360, verify=False)
        if method == 'POST':
            response = requests.post(settings.AMP_URL + url, json=kwargs, headers=headers, timeout=360, verify=False)
        if method == 'PUT':
            response = requests.put(settings.AMP_URL + url, json=kwargs, headers=headers, timeout=360, verify=False)
        if method == 'DELETE':
            response = requests.delete(settings.AMP_URL + url, json=kwargs, headers=headers, timeout=360, verify=False)
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
