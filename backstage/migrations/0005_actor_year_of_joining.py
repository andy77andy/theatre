# Generated by Django 4.2.2 on 2023-06-13 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstage', '0004_alter_actor_options_rename_award_actor_awards_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='year_of_joining',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
