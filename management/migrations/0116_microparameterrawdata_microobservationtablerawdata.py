# Generated by Django 4.1 on 2023-07-13 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0115_alter_microobservationtable_first_exponent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MicroParameterRawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_condition_of_sample', models.CharField(max_length=500, null=True)),
                ('media_used', models.CharField(max_length=500, null=True)),
                ('prepared_dilution', models.CharField(max_length=500, null=True)),
                ('diluent_used', models.CharField(max_length=500, null=True)),
                ('positive_control_used', models.CharField(max_length=500, null=True)),
                ('negative_control_used', models.CharField(max_length=500, null=True)),
                ('date_of_incubation', models.DateTimeField(null=True)),
                ('required_temperature', models.CharField(max_length=500, null=True)),
                ('parameter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.testresult')),
                ('sample_form', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_detail_rawdata', to='management.sampleform')),
                ('sample_form_has_parameter', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_detail_sample_form_has_parameter_rawdata', to='management.sampleformhasparameter')),
            ],
        ),
        migrations.CreateModel(
            name='MicroObservationTableRawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation_number', models.CharField(blank=True, max_length=500, null=True)),
                ('observation_time', models.CharField(blank=True, max_length=500, null=True)),
                ('temperature', models.CharField(blank=True, max_length=500, null=True)),
                ('time', models.CharField(blank=True, max_length=500, null=True)),
                ('first_exponent', models.CharField(blank=True, max_length=500, null=True)),
                ('first_exponent_a', models.CharField(blank=True, max_length=500, null=True)),
                ('first_exponent_b', models.CharField(blank=True, max_length=500, null=True)),
                ('second_exponent', models.CharField(blank=True, max_length=500, null=True)),
                ('second_exponent_a', models.CharField(blank=True, max_length=500, null=True)),
                ('second_exponent_b', models.CharField(blank=True, max_length=500, null=True)),
                ('third_exponent', models.CharField(blank=True, max_length=500, null=True)),
                ('third_exponent_a', models.CharField(blank=True, max_length=500, null=True)),
                ('third_exponent_b', models.CharField(blank=True, max_length=500, null=True)),
                ('negative_control', models.CharField(blank=True, max_length=500, null=True)),
                ('positive_control', models.CharField(blank=True, max_length=500, null=True)),
                ('micro_parameter_table', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_observation_table_rawdata', to='management.microparameter')),
                ('parameter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.testresult')),
                ('sample_form', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_observation_table_rawdata', to='management.sampleform')),
            ],
        ),
    ]
