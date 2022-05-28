""" Here we gather all configuration for an agents from different models sinto single JSON object. """

from django.conf import settings
from pbxsetup.models import SIPUser, Settings


# const configuration = {
#   sockets: [],
#   uri: 'sip:webrtc_client2@webtel.cloud',
#   realm: 'webrtc_md5_test',
#   ha1: 'e9cfcf3bd936f2103d077c172af2eb6f',
#   wss: 'wss://webtel.cloud:8089/ws',
#   openedWindowTitle: 'webtel.cloud',
#   extension: 'sip:200@webtel.cloud',
# };

def webtel_params(username: str) -> dict:
    try:
        agent = SIPUser.objects.get(username=username)

    except SIPUser.DoesNotExist:
        return None

    try:
        settings = Settings.objects.first()

    except Settings.DoesNotExist:
        return None

    # Allowed to use web provided configuration only for webphone
    if agent.transport.protocol != 'wss':
        return None

    return {
        'uri': 'sip:{}@{}'.format(agent.username, settings.domain),
        'realm': agent.realm,
        'ha1': agent.md5_cred,
        'wss': settings.wss_url,
        'openedWindowTitle': 'webtel.cloud',
        'extension': 'sip:{}@{}'.format(agent.allowed_extension, settings.domain),
    }


def django_user_params(username: str) -> dict:
    try:
        user = SIPUser.objects.get(username=username)

    except SIPUser.DoesNotExist:
        return None

    try:
        settings = Settings.objects.first()

    except Settings.DoesNotExist:
        return None

    # Allowed to use web provided configuration only for webphone
    if user.transport.protocol != 'wss':
        return None

    return {
        'uri': 'sip:{}@{}'.format(user.username, settings.domain),
        'realm': user.realm,
        'ha1': user.md5_cred,
        'wss': settings.wss_url,
    }
