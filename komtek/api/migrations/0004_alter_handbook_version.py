# Generated by Django 3.2.5 on 2021-07-13 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_item_handbook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handbook',
            name='version',
            field=models.CharField(max_length=100, verbose_name='Версия'),
        ),
    ]