# Generated by Django 4.1 on 2024-02-23 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0192_sampleformhaveinspector_feed_owner_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleformhaveinspector',
            name='remarks',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
