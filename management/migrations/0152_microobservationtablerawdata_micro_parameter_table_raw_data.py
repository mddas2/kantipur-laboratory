# Generated by Django 4.1 on 2023-08-09 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0151_remove_microobservationtablerawdata_micro_parameter_table_raw_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='microobservationtablerawdata',
            name='micro_parameter_table_raw_data',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_observation_table_raw_data', to='management.microparameterrawdata'),
        ),
    ]