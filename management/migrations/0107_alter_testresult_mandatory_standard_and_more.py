# Generated by Django 4.1 on 2023-07-11 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0106_microobservationtable_micro_parameter_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='mandatory_standard',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testresult',
            name='mandatory_standard_nepali',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
