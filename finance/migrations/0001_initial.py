# Generated by Django 5.0.6 on 2024-12-27 13:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bazar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Fund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='فنڈ کا نام')),
                ('fund_type', models.CharField(choices=[('TH1', 'جمعرات پہلا وقت'), ('TH2', 'جمعرات دوسرا وقت'), ('FR', 'جمعہ فنڈ'), ('MS', 'مولوی کی ماہانہ تنخواہ'), ('OF', 'دیگر فنڈز')], max_length=10, verbose_name='فنڈ کی قسم')),
                ('description', models.TextField(blank=True, null=True, verbose_name='تفصیل')),
            ],
        ),
        migrations.CreateModel(
            name='Withdrawal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('salary', 'مولوی کی تنخواہ'), ('electricity_bill', 'بجلی کا بل'), ('other_expense', 'دیگر اخراجات')], max_length=20, verbose_name='اخراجات کی قسم')),
                ('expense_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='اخراجات کا نام')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='رقم')),
                ('date', models.DateField(auto_now_add=True, verbose_name='تاریخ')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='رقم')),
                ('date', models.DateField(auto_now_add=True, verbose_name='تاریخ')),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.fund', verbose_name='فنڈ')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('deposit_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
                ('bazar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.bazar')),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.CharField(max_length=20, verbose_name='مہینہ')),
                ('year', models.IntegerField(verbose_name='سال')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='تنخواہ کی رقم')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.person', verbose_name='شخص')),
            ],
        ),
    ]
