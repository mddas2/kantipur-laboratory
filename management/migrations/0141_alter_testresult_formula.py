# Generated by Django 4.1 on 2023-08-06 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0140_alter_microparameter_prepared_dilution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testresult',
            name='formula',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
