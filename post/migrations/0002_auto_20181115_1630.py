# Generated by Django 2.1.2 on 2018-11-15 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='photos/%Y/%m/%d/'),
        ),
    ]