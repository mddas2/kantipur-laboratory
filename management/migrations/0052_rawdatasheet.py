# Generated by Django 4.1 on 2023-06-23 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0051_sampleformhasparameter_remarks_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='rawDataSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_form', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='raw_datasheet', to='management.sampleform')),
                ('sample_form_has_parameter', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='raw_datasheet', to='management.sampleformhasparameter')),
            ],
        ),
    ]
