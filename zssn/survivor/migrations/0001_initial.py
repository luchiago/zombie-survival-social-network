# Generated by Django 2.1.4 on 2018-12-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survivor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(choices=[('M', 'MALE'), ('F', 'FEMALE'), ('O', 'Other')], max_length=1)),
                ('last_location_longitude', models.CharField(max_length=12)),
                ('last_location_latitude', models.CharField(max_length=11)),
                ('infected', models.BooleanField(default=False)),
                ('water', models.IntegerField()),
                ('food', models.IntegerField()),
                ('medication', models.IntegerField()),
                ('ammunition', models.IntegerField()),
            ],
        ),
    ]