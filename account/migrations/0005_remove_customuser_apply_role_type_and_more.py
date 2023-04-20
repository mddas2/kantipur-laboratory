# Generated by Django 4.1 on 2023-04-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_remove_customuser_sex_alter_customuser_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='apply_role_type',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(null=True, upload_to='user/profile'),
        ),
    ]
