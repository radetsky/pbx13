# Generated by Django 4.0.1 on 2022-01-07 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbxsetup', '0011_alter_sippeer_options_alter_siptransport_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_template', models.TextField(default='type=endpoint\n        context=Long-Distance\n        allow= !all, g722, ulaw\n        direct_media=no\n        trust_id_outbound=yes\n        device_state_busy_at=1\n        dtmf_mode=rfc4733\n        transport=transport-udp-nat\n        rtp_symmetric=yes\n        force_rport=yes\n        rewrite_contact=yes', help_text='You may override it by custom settings in user form', verbose_name='User basic template')),
            ],
        ),
    ]