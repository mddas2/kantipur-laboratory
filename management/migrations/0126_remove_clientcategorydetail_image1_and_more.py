# Generated by Django 4.1 on 2023-07-23 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0125_clientcategorydetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image1',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image10',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image2',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image3',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image4',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image5',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image6',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image7',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image8',
        ),
        migrations.RemoveField(
            model_name='clientcategorydetail',
            name='image9',
        ),
        migrations.CreateModel(
            name='ClientCategoryDetailImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(null=True, upload_to='uploads/clientcategorydetailimages')),
                ('client_category_detail', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ClientCategoryDetail', to='management.clientcategorydetail')),
            ],
        ),
    ]