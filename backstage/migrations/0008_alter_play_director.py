# Generated by Django 4.2.2 on 2023-06-15 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "backstage",
            "0007_alter_actor_options_alter_award_options_play_genre_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="play",
            name="director",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="plays",
                to="backstage.director",
            ),
        ),
    ]
