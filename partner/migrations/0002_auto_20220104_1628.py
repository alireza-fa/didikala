# Generated by Django 3.2 on 2022-01-04 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20220104_1628'),
        ('partner', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'verbose_name': 'فروشنده', 'verbose_name_plural': 'فروشندگان'},
        ),
        migrations.AlterModelOptions(
            name='partnerstock',
            options={'ordering': ('price',), 'verbose_name': 'قیمت فروشنده', 'verbose_name_plural': 'قیمت فروشندگان'},
        ),
        migrations.AlterField(
            model_name='partner',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='description',
            field=models.TextField(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='modified',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ تغییرات'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='name',
            field=models.CharField(max_length=120, verbose_name='اسم'),
        ),
        migrations.AlterField(
            model_name='partnerstock',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='partner.partner', verbose_name='فروشنده'),
        ),
        migrations.AlterField(
            model_name='partnerstock',
            name='price',
            field=models.BigIntegerField(verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='partnerstock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='catalogue.product', verbose_name='محصول'),
        ),
    ]