# Generated by Django 4.2.2 on 2023-07-04 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstage', '0016_award_play_delete_playaward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='play',
            name='on_stage',
            field=models.BooleanField(default=True),
        ),
    ]