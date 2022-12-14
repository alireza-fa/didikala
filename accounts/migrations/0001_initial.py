# Generated by Django 3.2 on 2021-12-27 02:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=32, null=True)),
                ('last_name', models.CharField(blank=True, max_length=32, null=True)),
                ('fullname', models.CharField(blank=True, max_length=64, null=True)),
                ('code_melli', models.CharField(blank=True, max_length=20, null=True)),
                ('card_number', models.CharField(blank=True, max_length=20, null=True)),
                ('received_news', models.BooleanField(default=False)),
                ('phone_number', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='profiles/%Y/%m/%d/')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=32, null=True)),
                ('foreign_person', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserMassage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=120)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='massages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-user',),
            },
        ),
    ]
