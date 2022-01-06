from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def pjsip_conf(request):

    conf = "pjsip.conf"
    return HttpResponse(conf)
