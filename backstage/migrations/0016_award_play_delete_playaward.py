# Generated by Django 4.2.2 on 2023-07-03 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("backstage", "0015_alter_award_options_remove_award_play_playaward"),
    ]

    operations = [
        migrations.AddField(
            model_name="award",
            name="play",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="play_awards",
                to="backstage.play",
            ),
        ),
        migrations.DeleteModel(
            name="PlayAward",
        ),
    ]
