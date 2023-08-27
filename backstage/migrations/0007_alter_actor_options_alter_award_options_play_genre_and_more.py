# Generated by Django 4.2.2 on 2023-06-15 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("backstage", "0006_alter_actor_awards"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="actor",
            options={"ordering": ["last_name"], "verbose_name_plural": "actors"},
        ),
        migrations.AlterModelOptions(
            name="award",
            options={"ordering": ["name"]},
        ),
        migrations.AddField(
            model_name="play",
            name="genre",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="actors",
                to="backstage.genre",
            ),
        ),
        migrations.AlterField(
            model_name="director",
            name="awards",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="director_awards",
                to="backstage.award",
            ),
        ),
        migrations.AlterField(
            model_name="play",
            name="awards",
            field=models.ManyToManyField(
                blank=True, related_name="awards", to="backstage.award"
            ),
        ),
        migrations.AlterField(
            model_name="play",
            name="director",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="actors",
                to="backstage.director",
            ),
        ),
    ]
