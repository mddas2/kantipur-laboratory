# Generated by Django 4.1 on 2023-07-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0029_customuser_is_reject'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_recheck',
            field=models.BooleanField(default=False),
        ),
    ]