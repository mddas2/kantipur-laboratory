# Generated by Django 4.1 on 2024-02-23 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0193_sampleformhaveinspector_remarks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformhaveinspector',
            name='feed_owner_name',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sampleformhaveinspector',
            name='preservatives_details_and_quantity',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sampleformhaveinspector',
            name='remarks',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sampleformhaveinspector',
            name='sample_collected_address',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
