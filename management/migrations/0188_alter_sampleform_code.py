# Generated by Django 4.1 on 2024-02-21 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0187_remove_sampleform_remarks_recheck_verifier_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='code',
            field=models.IntegerField(null=True),
        ),
    ]
