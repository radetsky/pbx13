from django.http import HttpResponse
import pbxsetup.conf as conf

from pbxsetup.ael import make_extensions_ael


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def pjsip_conf(request):
    '''
    I will not rubbish HTTP handlers functions.
    Using internal modules to do dirty job.
    '''
    plaintext = conf.make_pjsip_conf()
    return HttpResponse(plaintext, content_type='text/plain')


def extensions_ael(request):
    '''
    I will not rubbish HTTP handlers functions.
    Using internal modules to do dirty job.
    '''
    plaintext = make_extensions_ael()
    return HttpResponse(plaintext, content_type='text/plain')
