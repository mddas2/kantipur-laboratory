# Generated by Django 4.1 on 2023-06-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0069_testresult_mandatory_standard_nepali_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='notation',
            field=models.CharField(max_length=100, null=True),
        ),
    ]