# Generated by Django 3.0.3 on 2020-03-05 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('co_working_space', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='money',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='seatbooking',
            name='total_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='topuplog',
            name='amount',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='zone',
            name='price',
            field=models.IntegerField(),
        ),
    ]
