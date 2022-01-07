from django.contrib import admin

# Register your models here.
from .models import SIPTransport, SIPUser, SIPPeer, Settings
from .forms import SIPPeerForm, SIPUserForm


class SIPUserAdmin(admin.ModelAdmin):
    form = SIPUserForm
    list_display = ('name', 'username', 'extension')
    ordering = ['name', 'username', 'extension']


class SIPPeerAdmin(admin.ModelAdmin):
    form = SIPPeerForm
    list_display = ('name', 'description')
    ordering = ['name', 'description']


class SIPTransportAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Generic', {'fields': ['description', 'name']}),
        ('Network settings', {'fields': [
            'protocol',
            'bind',
            'local_nets',
            'external_media_address',
            'external_signaling_address']}),
        ('TLS Settings (only if TLS protocol is used)', {'fields': [
            'method', 'cert_file', 'priv_key_file', 'ca_list_file'
        ]})
    ]
    list_display = ('name', 'description')
    ordering = ['name', 'description']


admin.site.register(SIPUser, SIPUserAdmin)
admin.site.register(SIPPeer, SIPPeerAdmin)
admin.site.register(SIPTransport, SIPTransportAdmin)
admin.site.register(Settings)
