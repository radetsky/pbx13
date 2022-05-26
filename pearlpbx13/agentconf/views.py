from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings

"""
This is an app that returns configuration files for an agents.
"""


@csrf_exempt if settings.DEBUG else csrf_protect
@require_POST
def webtel(request):
    return HttpResponse("Hello, world. You're at the polls index.")
