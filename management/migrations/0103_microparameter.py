# Generated by Django 4.1 on 2023-07-11 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0102_alter_sampleform_days_dfb'),
    ]

    operations = [
        migrations.CreateModel(
            name='MicroParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.testresult')),
                ('sample_form', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_detail', to='management.sampleform')),
                ('sample_form_has_parameter', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='micro_detail_sample_form_has_parameter', to='management.sampleformhasparameter')),
            ],
        ),
    ]
