# Generated by Django 4.0.5 on 2022-06-28 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='owner',
            new_name='seller',
        ),
    ]
