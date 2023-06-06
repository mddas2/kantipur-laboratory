# Generated by Django 4.1 on 2023-06-06 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0026_alter_sampleformverifier_sample_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sampleform',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'pending'), ('approved', 'approved'), ('processing', 'processing'), ('completed', 'completed'), ('verified', 'verified'), ('reject', 'reject')], max_length=155, null=True),
        ),
    ]
