# Generated by Django 4.0.1 on 2022-03-28 21:27

from django.db import migrations, models
import pbxsetup.validators


class Migration(migrations.Migration):

    dependencies = [
        ('pbxsetup', '0012_settings'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='settings',
            options={'verbose_name_plural': '99. General Settings'},
        ),
        migrations.AlterField(
            model_name='settings',
            name='user_template',
            field=models.TextField(default='type = endpoint\ncontext = default\nallow = !all, g722, ulaw, alaw\ndirect_media = no\ntrust_id_outbound = yes\ndevice_state_busy_at = 1\ndtmf_mode = rfc4733\ntransport = transport-udp-nat\nrtp_symmetric = yes\nforce_rport = yes\nrewrite_contact = yes', help_text='You may override it by custom settings in user form', verbose_name='User basic template'),
        ),
        migrations.AlterField(
            model_name='siptransport',
            name='bind',
            field=models.GenericIPAddressField(default='0.0.0.0', validators=[pbxsetup.validators.validate_bind_ip]),
        ),
    ]
