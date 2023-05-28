# Generated by Django 4.1 on 2023-05-28 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_customuser_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'SUPERADMIN'), (2, 'SMU'), (3, 'SUPERVISOR'), (4, 'ANALYST'), (5, 'USER'), (6, 'VERIFIER')], null=True),
        ),
    ]
