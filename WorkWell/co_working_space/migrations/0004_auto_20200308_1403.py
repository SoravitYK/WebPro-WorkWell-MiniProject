# Generated by Django 3.0.4 on 2020-03-08 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('co_working_space', '0003_auto_20200308_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatbooking',
            name='total_price',
            field=models.IntegerField(null=True),
        ),
    ]
