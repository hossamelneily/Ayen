# Generated by Django 3.1.2 on 2020-10-18 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='mobile_number',
        ),
        migrations.AddField(
            model_name='account',
            name='occupation',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Occupation'),
        ),
    ]
