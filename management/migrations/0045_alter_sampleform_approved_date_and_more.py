# Generated by Django 4.1 on 2023-06-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0044_sampleform_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='approved_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='sampleform',
            name='completed_date',
            field=models.DateTimeField(null=True),
        ),
    ]
