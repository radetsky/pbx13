from django.db import models
import django.db.models.deletion as deletion
from .validators import validate_bind_ip
from hashlib import md5


class SIPTransport(models.Model):
    PROTOCOL_CHOICES = [
        ('udp', 'UDP'),
        ('tcp', 'TCP'),
        ('tls', 'TLS'),
        ('wss', 'WSS'),
    ]

    METHOD_CHOICES = [
        ('default', 'The default as defined by PJSIP. This is currently TLSv1'),
        ('tlsv1',   'TLSv1'),
        ('tlsv1_1', 'TLSv1.1'),
        ('tlsv1_2', 'TLSv1.2'),
        ('sslv2',   'SSLv2'),
        ('sslv3',   'SSLv3'),
        ('sslv23',  'SSLv2.3'),
    ]

    description = models.CharField(default="", max_length=64,
                                   help_text="Example: UDP + NAT for remote users",
                                   verbose_name='Description', blank=True)
    name = models.CharField(max_length=32, unique=True, null=False, blank=False,
                            default="", help_text="Example: transport-udp-nat",
                            verbose_name="Name")
    protocol = models.CharField(
        max_length=3, null=False, choices=PROTOCOL_CHOICES, default='udp', blank=False)

    bind = models.CharField(validators=[validate_bind_ip],
                            default="0.0.0.0", null=False, blank=False, max_length=256)
    local_nets = models.CharField(null=True, blank=True, max_length=256,
                                  verbose_name="local_net",
                                  help_text="List all local networks splitted by comma: 10.0.0.0/16, 192.168.0.0/24")
    external_media_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="This is the external IP address to use in RTP handling",
        verbose_name="External RTP IP address")
    external_signaling_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="This is much like the external_media_address setting, but for SIP signaling instead of RTP media.",
        verbose_name="External SIP IP address"
    )
    method = models.CharField(
        max_length=10, null=False, choices=METHOD_CHOICES, default='default', blank=False
    )

    # Contents of files, not names. We will generate filenames later. It doesn't matter.
    # TODO: реализовать форму под них.
    cert_file = models.TextField(blank=True, null=False)
    priv_key_file = models.TextField(blank=True, null=False)
    ca_list_file = models.TextField(blank=True, null=False)

    # various TLS specific options below:
    # cipher - do not use in UI "until it sleeps". Too many values. Users usually do not know it.

    class Meta:
        verbose_name_plural = "1. SIP Transports"


class SIPUser(models.Model):

    name = models.CharField(default="", max_length=64, blank=False,
                            help_text='Full name of user, description of connection', verbose_name='Name')
    username = models.CharField(max_length=32, unique=True, null=False, blank=False,
                                help_text='Username: 3-32 characters', verbose_name='Username')
    secret = models.CharField(max_length=32, unique=True, null=False, blank=False,
                              help_text='Password for the connection', verbose_name='Password')
    transport = models.ForeignKey(
        SIPTransport, related_name='sip_user_transport', on_delete=deletion.PROTECT, null=True, blank=False)
    extension = models.CharField(max_length=32, unique=True, null=True, blank=False,
                                 help_text='Easy way to setup internal extension for the user', verbose_name='Extension')

    allowed_extension = models.CharField(max_length=32, unique=False, null=True, blank=False, default='s',
                                         help_text='Only one allowed extension for the user', verbose_name='Allowed extension')

    custom_settings = models.TextField(null=True, blank=False, default="",
                                       help_text='Custom user settings', verbose_name='Settings')
    custom_auth_settings = models.TextField(null=True, blank=False, default="",
                                            help_text='Custom user [auth] section', verbose_name='Auth Settings')

    custom_aor_settings = models.TextField(null=True, blank=False, default="",
                                           help_text='Custom user [aor] section', verbose_name='AOR Settings')

    @property
    def realm(self):
        return f'{self.transport.protocol}-{self.username}'

    @property
    def md5_cred(self):
        return md5(f'{self.username}:{self.secret}:{self.realm}'.encode('utf-8')).hexdigest()

    class Meta:
        verbose_name_plural = "2. SIP Users"


class SIPPeer(models.Model):
    description = models.CharField(
        default="", max_length=64, help_text='Describe a peer', verbose_name='Description')
    name = models.CharField(max_length=32, unique=True, null=False,
                            default="", help_text='Name of the channel', verbose_name='Channel name')
    username = models.CharField(
        max_length=32, unique=True, null=False, default="",
        help_text='Username for the connection used for remote side', verbose_name='Username')
    secret = models.CharField(
        max_length=32, unique=True, null=False, default="",
        help_text='Clear text password for the connection used for remote side',
        verbose_name='Password')

    host_port = models.CharField(
        max_length=256, null=False, blank=False, default="",
        help_text='Host:Port of the peer. Port is optional.', verbose_name='Host:Port')

    registrationHere = models.BooleanField(
        default=False,
        help_text='Should remote peer register here? Used for GSM, E1, T1, FXS, FXO gateways, etc. ',
        verbose_name='Registration here')
    registrationThere = models.BooleanField(
        default=False, help_text='Should we register on remote service? Typically used for providers',
        verbose_name='Registration there')

    callLimit = models.SmallIntegerField(
        default=0, help_text='Maximum calls on the trunk', verbose_name='Call Limit')
    transport = models.ForeignKey(
        SIPTransport, related_name='sip_peer_transport', on_delete=deletion.PROTECT, null=True, blank=False)

    class Meta:
        verbose_name_plural = "3. SIP Uplinks and Peers"


class DialplanContext(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False, blank=False,
                            verbose_name='Context name', help_text='Use latin symbols, digits and undercore')
    description = models.CharField(max_length=64, unique=False, null=False, blank=True,
                                   verbose_name='Context description', help_text='Use latin symbols, digits and undercore to describe')

    class Meta:
        db_table = 'diaplan_contexts'
        verbose_name_plural = "4. Dialplan contexts"


class DialplanExtension(models.Model):
    context = models.ForeignKey(DialplanContext, related_name='Context',
                                on_delete=deletion.PROTECT, null=True, blank=False)
    ext = models.CharField(max_length=32, unique=False, null=False, blank=False,
                           default='_X!', verbose_name='Extension', help_text='Asterisk extension')
    dialplan = models.TextField(verbose_name='Extension scenario')
    description = models.CharField(max_length=64, unique=False, null=False, blank=True,
                                   verbose_name='Extension description', help_text='Use latin symbols, digits and undercore to describe')

    @property
    def context_name(self):
        return self.context.name

    class Meta:
        db_table = 'dialplan_extensions'
        verbose_name_plural = "5. Dialplan extensions"

        constraints = [
            models.UniqueConstraint(
                fields=['context', 'ext'], name='unique extension inside context')
        ]


class DialplanMacro(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False, blank=False,
                            verbose_name='Macro name', help_text='Use latin symbols, digits and undercore')
    description = models.CharField(max_length=64, unique=False, null=False, blank=True,
                                   verbose_name='Macro description', help_text='Use latin symbols, digits and undercore to describe')
    macro = models.TextField(verbose_name='Macro scenario')

    class Meta:
        db_table = 'dialplan_macros'
        verbose_name_plural = "6. Dialplan macros"


class Settings(models.Model):
    domain = models.CharField(
        max_length=64, unique=True, null=False, blank=False, default="webtel.cloud", verbose_name="Hostname of the server", help_text="Hostname of the server")

    wss_port = models.SmallIntegerField(default=8089, null=False, blank=False,
                                        verbose_name="WSS port of the server", help_text="WSS port of the server")

    @ property
    def wss_url(self):
        return f'wss://{self.domain}:{self.wss_port}/ws'

    user_template = models.TextField(
        default='''type = endpoint
context = default
allow = !all, g722, ulaw, alaw
direct_media = no
trust_id_outbound = yes
device_state_busy_at = 1
dtmf_mode = rfc4733
transport = transport-udp-nat
rtp_symmetric = yes
force_rport = yes
rewrite_contact = yes''',
        verbose_name='User basic template',
        help_text='You may override it by custom settings in user form')

    user_aor_template = models.TextField(
        default='''type = aor
max_contacts = 1
remove_existing = yes''',
        verbose_name='User AOR template',
        help_text='You may override it by custom settings in user form'
    )

    user_auth_template = models.TextField(
        default='''type = auth
auth_type = md5''',
        verbose_name='User auth template',
        help_text='You may override it by custom settings in user form'
    )

    webrtc_template = models.TextField(
        default='''
dtls_auto_generate_cert=yes
webrtc=yes
context=default
max_audio_streams = 1
max_video_streams = 15
disallow=all
allow=opus,g722,ulaw,vp9,vp8,h264''',
        verbose_name='WebRTC template for endpoint',
        help_text='You may override it by custom settings in user form'
    )

    webrtc_aor_template = models.TextField(
        default='''type = aor
max_contacts = 15
remove_existing = yes''',
        verbose_name='WebRTC AOR template',
        help_text='You may override it by custom settings in user form'
    )

    webrtc_auth_template = models.TextField(
        default='''type = auth
auth_type = md5''',
        verbose_name='WebRTC auth template',
        help_text='You may override it by custom settings in user form'
    )

    def save(self, *args, **kwargs):
        self.pk = self.id = 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "99. General Settings"
