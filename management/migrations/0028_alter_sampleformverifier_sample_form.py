# Generated by Django 4.1 on 2023-06-06 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0027_alter_sampleform_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleformverifier',
            name='sample_form',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='verifier', to='management.sampleform'),
        ),
    ]
