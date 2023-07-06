# Generated by Django 4.1 on 2023-07-06 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_customuser_test_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'SUPERADMIN'), (2, 'SMU'), (3, 'SUPERVISOR'), (4, 'ANALYST'), (5, 'USER'), (6, 'VERIFIER'), (7, 'ADMIN')], null=True),
        ),
    ]
