# Generated by Django 4.1 on 2024-03-04 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0044_customuser_is_public_analyst'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nepali_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='position_nepali',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]