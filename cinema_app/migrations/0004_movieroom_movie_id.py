# Generated by Django 2.2.2 on 2019-06-29 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_app', '0003_remove_movieroom_movieroom_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movieroom',
            name='Movie_ID',
            field=models.IntegerField(default=930000),
            preserve_default=False,
        ),
    ]
