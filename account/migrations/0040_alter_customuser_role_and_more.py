# Generated by Django 4.1 on 2024-02-20 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0039_userhaveinspector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'SUPERADMIN'), (2, 'SMU'), (3, 'SUPERVISOR'), (4, 'ANALYST'), (5, 'USER'), (6, 'VERIFIER'), (7, 'ADMIN'), (8, 'INSPECTOR')], null=True),
        ),
        migrations.AlterField(
            model_name='userhaveinspector',
            name='government_issued_document',
            field=models.FileField(blank=True, upload_to='media/user/inspector'),
        ),
    ]
