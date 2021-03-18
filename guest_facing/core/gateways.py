import requests
import json
import logging
from datetime                   import datetime as dt
from json                       import JSONDecodeError
from django.conf                import settings
from django.utils.translation   import gettext, gettext_lazy as _

logger = logging.getLogger('gateways')


# guest facing endpoint gateway
def guest_endpoint(url, property_id, post_data):
    prop = next((prop_data for prop_data in settings.GUEST_ENDPOINT or [] if prop_data.get('id') == property_id), None)
    url = prop.get('url', '') + url
    post_data['api_key'] = prop.get('key', '')
    post_data['site_id'] = prop.get('id', '')
    post_data['site_name'] = prop.get('name', '')
    try:
        logger.info('REQUEST ' + str(url) + ' ' + json.dumps(post_data))
        response = requests.post(url, json=post_data, timeout=prop.get('timeout', 30), verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Unable to connect to server, please try again.')}
    logger.info('RESPONSE ' + json.dumps(json_response))
    return json_response


# AMP endpoint gateway
def amp_endpoint(url, property_id):
    prop = next((prop_data for prop_data in settings.AMP_ENDPOINT or [] if prop_data.get('id') == property_id), None)
    url = prop.get('url', '') + url
    post_data = {}
    post_data['api_key'] = prop.get('key', '')
    post_data['site_id'] = prop.get('id', '')
    post_data['site_name'] = prop.get('name', '')
    try:
        logger.info('REQUEST ' + str(url) + ' ' + json.dumps(post_data))
        response = requests.post(url, json=post_data, timeout=prop.get('timeout', 30), verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Unable to connect to server, please try again.')}
    logger.info('RESPONSE ' + json.dumps(json_response))
    return json_response


# ocr scanning
def ocr(image_file, scan_type):
    url = settings.OCR_ENDPOINT_URL + scan_type
    files = {scan_type: open(image_file, 'rb')}
    data = {'api_key': settings.OCR_ENDPOINT_KEY}
    try:
        logger.info('REQUEST ' + str(url))
        response = requests.post(url, files=files, data=data, timeout=settings.OCR_ENDPOINT_TIMEOUT_LIMIT)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'status': 'error', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'status': 'error', 'message': _('Error connecting to server')}
    logger.info('RESPONSE ' + json.dumps(json_response))
    return json_response
