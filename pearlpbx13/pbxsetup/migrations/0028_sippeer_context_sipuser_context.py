# Generated by Django 4.0.4 on 2022-07-11 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbxsetup', '0027_dialplanmacro_alter_dialplancontext_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sippeer',
            name='context',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sip_peer_context', to='pbxsetup.dialplancontext'),
        ),
        migrations.AddField(
            model_name='sipuser',
            name='context',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sip_user_context', to='pbxsetup.dialplancontext'),
        ),
    ]
