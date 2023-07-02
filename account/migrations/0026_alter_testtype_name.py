# Generated by Django 4.1 on 2023-07-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0025_testtype_remove_customuser_test_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtype',
            name='name',
            field=models.CharField(choices=[('Chemical', 'Chemical'), ('Microbiological', 'Microbiological'), ('Instrumental', 'Instrumental')], default=None, max_length=155, null=True),
        ),
    ]
