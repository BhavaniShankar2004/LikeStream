# Generated by Django 5.0.6 on 2024-07-23 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='pro2.png', upload_to='profile_pics'),
        ),
    ]
