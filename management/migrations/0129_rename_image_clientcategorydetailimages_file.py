# Generated by Django 4.1 on 2023-07-23 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0128_alter_clientcategorydetail_client_sub_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clientcategorydetailimages',
            old_name='image',
            new_name='file',
        ),
    ]