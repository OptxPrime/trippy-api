# Generated by Django 3.2.5 on 2022-05-22 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('putovanja_app', '0005_tourregistrations_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourregistrations',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]