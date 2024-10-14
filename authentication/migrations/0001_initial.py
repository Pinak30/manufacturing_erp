# Generated by Django 4.1.13 on 2024-10-14 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=100)),
                ('role', models.CharField(max_length=30)),
                ('date_of_joining', models.DateField()),
            ],
        ),
    ]
