# Generated by Django 4.1 on 2023-05-29 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_remove_sampleform_commodity_id_sampleform_commodity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='commodity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sample_form', to='management.commodity'),
        ),
    ]
