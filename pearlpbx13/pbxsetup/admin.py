from django.contrib import admin

# Register your models here.
from .models import SIPTransport, SIPUser, SIPPeer, Settings, DialplanContext, DialplanExtension
from .forms import SIPPeerForm, SIPUserForm, DialplanExtensionForm


class SIPUserAdmin(admin.ModelAdmin):
    form = SIPUserForm
    list_display = ('name', 'username', 'extension')
    ordering = ['name', 'username', 'extension']
    search_fields = ['name', 'username', 'extension']


class SIPPeerAdmin(admin.ModelAdmin):
    form = SIPPeerForm
    list_display = ('name', 'description')
    ordering = ['name', 'description']
    search_fields = ['name', 'description']


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


class DialplanContextAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ('name', 'description')
    ordering = ['name', 'description']
    search_fields = ['name', 'description']


class DialplanExtensionAdmin(admin.ModelAdmin):
    form = DialplanExtensionForm
    fields = ['context', 'ext', 'dialplan', 'description']
    list_display = ('context_name', 'ext', 'description')
    ordering = ['context', 'ext']
    search_fields = ['ext', 'dialplan', 'description']


admin.site.register(SIPUser, SIPUserAdmin)
admin.site.register(SIPPeer, SIPPeerAdmin)
admin.site.register(SIPTransport, SIPTransportAdmin)
admin.site.register(DialplanContext, DialplanContextAdmin)
admin.site.register(DialplanExtension, DialplanExtensionAdmin)
admin.site.register(Settings)
