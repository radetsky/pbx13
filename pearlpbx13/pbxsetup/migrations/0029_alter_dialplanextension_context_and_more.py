# Generated by Django 4.0.4 on 2022-07-20 17:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pbxsetup', '0028_sippeer_context_sipuser_context'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dialplanextension',
            name='context',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='extensions', to='pbxsetup.dialplancontext'),
        ),
        migrations.AlterField(
            model_name='sipuser',
            name='allowed_extension',
            field=models.CharField(blank=True, default='', help_text='Only one allowed extension for the user', max_length=32, null=True, verbose_name='Allowed extension'),
        ),
    ]
