# Generated by Django 4.1.13 on 2024-09-26 15:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_document_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 26, 21, 24, 4, 251657)),
        ),
    ]
