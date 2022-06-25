from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from .agentconf import webtel_params, django_user_params

from pythemis.scell import SCellSeal


import logging
import json
import base64


"""
This is an app that returns configuration files for an agents.
"""


logger = logging.getLogger(__name__)
WEBTEL_SYNC_PREFIX = b'webtel-sync-'


@csrf_exempt if settings.DEBUG else csrf_protect
@require_POST
def webtel(request):
    # Consider that in the future we will have Base64 encoded string
    json_data = json.loads(request.body)
    print(json_data)
    try:
        b64data = json_data['username']
        data = json.loads(base64.b64decode(b64data))
        username = data['username']
        b64symkey = data['key']

    except KeyError:
        return HttpResponse('{"error": "username is required"}', content_type='application/json')

    user_params = webtel_params(username)
    if user_params is None:
        return HttpResponse('{"error": "username is required"}', content_type='application/json')

    user_params['status'] = 'ok'
    result = str.encode(json.dumps(user_params))

    symkey = base64.b64decode(b64symkey)
    cell = SCellSeal(key=symkey)
    encrypted_result = cell.encrypt(result, WEBTEL_SYNC_PREFIX)
    b64encoded_result = base64.b64encode(encrypted_result)
    return HttpResponse(b64encoded_result, content_type='text/plain')


@csrf_protect
@require_POST
def django_user(request):
    # Consider that in the future we will have Base64 encoded string
    json_data = json.loads(request.body)
    print(json_data)
    try:
        username = json_data['username']
    except KeyError:
        return HttpResponse('{"error": "username is required"}', content_type='application/json')

    user_params = django_user_params(username)
    if user_params is None:
        return HttpResponse('{"error": "username is required"}', content_type='application/json')

    user_params['status'] = 'ok'

    return HttpResponse(json.dumps(user_params), content_type='application/json')
