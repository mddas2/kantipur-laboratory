# Generated by Django 4.1 on 2023-07-11 08:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0096_alter_sampleform_report_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='sample_form',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments_sample_form', to='management.sampleform'),
        ),
    ]
