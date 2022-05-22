# Generated by Django 3.2.5 on 2022-05-22 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('putovanja_app', '0002_solotrip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solotrip',
            name='lat',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='solotrip',
            name='lng',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.CreateModel(
            name='GroupTour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=1024)),
                ('location_name', models.CharField(max_length=128)),
                ('lat', models.DecimalField(decimal_places=7, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=7, max_digits=10)),
                ('datetime', models.DateTimeField(verbose_name='tour datetime')),
                ('transport', models.CharField(max_length=64)),
                ('min_travelers', models.PositiveIntegerField()),
                ('max_travelers', models.PositiveIntegerField()),
                ('picture_url', models.URLField()),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='putovanja_app.agency')),
            ],
        ),
    ]