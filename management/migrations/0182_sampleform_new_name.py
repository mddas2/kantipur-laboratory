# Generated by Django 4.1 on 2023-12-13 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0181_noticeimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleform',
            name='new_name',
            field=models.CharField(max_length=255, null=True),
        ),
    ]