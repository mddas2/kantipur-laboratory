# Generated by Django 4.1 on 2023-07-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0116_microparameterrawdata_microobservationtablerawdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='microparameter',
            name='status',
            field=models.CharField(max_length=2000, null=True),
        ),
    ]
