# Generated by Django 3.2 on 2021-12-27 02:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_productfavorite_created'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productfavorite',
            options={'ordering': ('-created',)},
        ),
    ]