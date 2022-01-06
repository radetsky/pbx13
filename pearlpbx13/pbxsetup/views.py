from django.http import HttpResponse
import pbxsetup.conf as conf


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def pjsip_conf(request):
    '''
    I will not rubbish HTTP handlers functions.
    Using internal modules to do dirty job.
    '''
    plaintext = conf.make_pjsip_conf()
    return HttpResponse(plaintext, content_type='text/plain')
