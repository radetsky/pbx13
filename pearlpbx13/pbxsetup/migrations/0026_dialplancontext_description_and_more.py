# Generated by Django 4.0.4 on 2022-06-25 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pbxsetup', '0025_dialplanextension_dialplan'),
    ]

    operations = [
        migrations.AddField(
            model_name='dialplancontext',
            name='description',
            field=models.CharField(blank=True, help_text='Use latin symbols, digits and undercore to describe', max_length=64, verbose_name='Context description'),
        ),
        migrations.AddField(
            model_name='dialplanextension',
            name='description',
            field=models.CharField(blank=True, help_text='Use latin symbols, digits and undercore to describe', max_length=64, verbose_name='Extension description'),
        ),
        migrations.AlterField(
            model_name='dialplanextension',
            name='dialplan',
            field=models.TextField(verbose_name='Extension scenario'),
        ),
    ]