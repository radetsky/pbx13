# Generated by Django 4.0.1 on 2022-04-05 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbxsetup', '0015_remove_sippeer_registrationstring_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sippeer',
            name='host_port',
            field=models.CharField(default='', help_text='Host:Port of the peer. Port is optional.', max_length=256, verbose_name='Host:Port'),
        ),
    ]