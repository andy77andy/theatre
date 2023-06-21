# Generated by Django 4.2.2 on 2023-06-15 18:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstage', '0008_alter_play_director'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='troupe',
            field=models.ManyToManyField(related_name='plays', to=settings.AUTH_USER_MODEL),
        ),
    ]