# Generated by Django 4.1 on 2024-03-27 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtrack', '0007_alter_sampletrack_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampletrack',
            name='description',
            field=models.CharField(default='', max_length=4000, null=True),
        ),
        migrations.AlterField(
            model_name='sampletrack',
            name='remarks',
            field=models.CharField(default='', max_length=4000, null=True),
        ),
    ]
