# Generated by Django 4.1 on 2023-07-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0112_sampleformparameterformulacalculate_analyst_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='microobservationtable',
            name='negative_control',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='microobservationtable',
            name='positive_control',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
