import requests, json, logging
from datetime                   import datetime as dt
from json                       import JSONDecodeError
from django.conf                import settings
from django.core.cache          import cache
from django.utils.translation   import ugettext as _

logger = logging.getLogger('gateways')


# token for every endpoint
def token_endpoint(token_type):
    config = next((conf for conf in settings.TOKEN_ENDPOINT if conf.get('type') == token_type), {})
    method, auth, data, params, headers = 'post', (config.get('username'), config.get('password')), {'grant_type': 'client_credentials'}, {}, {}
    try:
        response = getattr(requests, method)(config.get('url', ''), auth=auth, data=data, params=params, timeout=config.get('timeout', 30), headers=headers, verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'statusCode': '522', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'statusCode': '522', 'message': _('Unable to connect to server, please try again.')}
    cache.set('token_%s' % token_type, json_response.get('access_token'), json_response.get('expires_in', 0))
    return json_response.get('access_token')


# guest facing endpoint gateway
def guest_endpoint(method, url, property_id, data={}):
    prop = next((prop_data for prop_data in settings.GUEST_ENDPOINT or [] if prop_data.get('id') == property_id), {})
    url = prop.get('url', '') + url
    data['siteId'] = prop.get('id', '')
    data['siteName'] = prop.get('name', '')
    params, headers = {}, {'Content-Type': 'application/json'}
    token_type = 'guest_facing'
    if method == 'get': # when `get` method, pass as params
        params = dict(data)
        data = {}
    try:
        logger.info('REQUEST %(method)s %(url)s %(data)s %(params)s' % {'method': method, 'url': url, 'data': json.dumps(data), 'params': json.dumps(params)})
        if not cache.get('token_%s' % token_type):
            token = token_endpoint(token_type)
        headers['Authorization'] = 'Bearer %s' % cache.get('token_%s' % token_type)
        response = getattr(requests, method)(url, data=json.dumps(data), params=params, timeout=prop.get('timeout', 30), headers=headers, verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'statusCode': '522', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'statusCode': '522', 'message': _('Unable to connect to server, please try again.')}
    logger.info('RESPONSE ' + json.dumps(json_response))
    return json_response


# AMP endpoint gateway
def amp_endpoint(method, url, property_id, data={}):
    prop = next((prop_data for prop_data in settings.AMP_ENDPOINT or [] if prop_data.get('id') == property_id), None)
    url = prop.get('url', '') + url
    data['siteId'] = prop.get('id', '')
    data['siteName'] = prop.get('name', '')
    params, headers = {}, {'Content-Type': 'application/json'}
    token_type = 'amp'
    if method == 'get': # when `get` method, pass as params
        params = dict(data)
        data = {}
    try:
        logger.info('REQUEST %(method)s %(url)s %(data)s %(params)s' % {'method': method, 'url': url, 'data': json.dumps(data), 'params': json.dumps(params)})
        if not cache.get('token_%s' % token_type):
            token = token_endpoint(token_type)
        headers['Authorization'] = 'Bearer %s' % cache.get('token_%s' % token_type)
        response = getattr(requests, method)(url, data=json.dumps(data), params=params, timeout=prop.get('timeout', 30), headers=headers, verify=False)
        response.raise_for_status()
        json_response = json.loads(response.content.decode('utf-8'))
    except requests.exceptions.HTTPError as http_error:
        try:
            json_response = json.loads(response.content.decode('utf-8'))
        except JSONDecodeError:
            json_response = {'statusCode': '522', 'message': response.content.decode('utf-8')}
    except requests.exceptions.RequestException as request_error:
        json_response = {'statusCode': '522', 'message': _('Unable to connect to server, please try again.')}
    logger.info('RESPONSE ' + json.dumps(json_response))
    return json_response


# ocr scanning
def ocr(image_file):
    url = settings.OCR_ENDPOINT_URL
    files = {'image': open(image_file, 'rb')}
    data, headers = {}, {'x-api-key': settings.OCR_ENDPOINT_KEY}
    data['selectionCode'] = ['']
    data['skipFaceDetect'] = ['']
    try:
        logger.info('REQUEST %(url)s' % {'url': url})
        response = requests.post(url, files=files, data=data, headers=headers, timeout=settings.OCR_ENDPOINT_TIMEOUT_LIMIT)
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
