# Generated by Django 3.2 on 2022-01-04 12:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
        migrations.AlterField(
            model_name='score',
            name='score',
            field=models.IntegerField(verbose_name='امتیاز'),
        ),
        migrations.AlterField(
            model_name='score',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='سن'),
        ),
        migrations.AlterField(
            model_name='user',
            name='card_number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره حساب'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='code_melli',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='کد ملی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True, unique=True, verbose_name='ایمیل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='نام'),
        ),
        migrations.AlterField(
            model_name='user',
            name='foreign_person',
            field=models.BooleanField(default=False, verbose_name='تبعه خارجی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fullname',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='نام و نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/%Y/%m/%d/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='کاربر فعال/غیر فعال'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='مدیر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='نام خانوادگی'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='شماره موبایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='received_news',
            field=models.BooleanField(default=False, verbose_name='عضویت در خبرنامه'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='نام کاربری'),
        ),
        migrations.AlterField(
            model_name='usermassage',
            name='body',
            field=models.TextField(verbose_name='متن'),
        ),
        migrations.AlterField(
            model_name='usermassage',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ پیام'),
        ),
        migrations.AlterField(
            model_name='usermassage',
            name='subject',
            field=models.CharField(max_length=120, verbose_name='موضوع'),
        ),
        migrations.AlterField(
            model_name='usermassage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='massages', to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
