# Generated by Django 4.1 on 2023-06-20 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websocket', '0005_notification_particular_message_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='group_notification',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]