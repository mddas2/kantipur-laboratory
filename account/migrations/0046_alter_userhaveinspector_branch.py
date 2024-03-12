# Generated by Django 4.1 on 2024-03-12 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('offices', '0003_branches_nepali_name'),
        ('account', '0045_customuser_nepali_name_customuser_position_nepali'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userhaveinspector',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offices.branches'),
        ),
    ]
