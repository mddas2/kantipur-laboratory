# Generated by Django 4.1 on 2023-06-18 08:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_customuser_department_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='department_address',
        ),
    ]