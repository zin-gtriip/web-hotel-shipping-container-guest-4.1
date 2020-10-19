import requests
import json
from json                       import JSONDecodeError
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _


# guest facing endpoint gateway
def guest_endpoint(url, post_data):
    post_data['api_key'] = settings.GUEST_ENDPOINT_KEY
    post_data['site_id'] = settings.GUEST_ENDPOINT_SITE_ID
    post_data['site_name'] = settings.GUEST_ENDPOINT_SITE_NAME
    try:
        response = requests.post(settings.GUEST_ENDPOINT_URL + url, json=post_data, timeout=30, verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Unable to connect to server, please try again.')}
    return json_response


# AMP endpoint gateway
def amp_endpoint(url):
    post_data = {}
    post_data['api_key'] = settings.AMP_ENDPOINT_KEY
    post_data['site_id'] = settings.AMP_ENDPOINT_SITE_ID
    post_data['site_name'] = settings.AMP_ENDPOINT_SITE_NAME
    try:
        response = requests.post(settings.AMP_ENDPOINT_URL + url, json=post_data, timeout=360, verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Unable to connect to server, please try again.')}
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
