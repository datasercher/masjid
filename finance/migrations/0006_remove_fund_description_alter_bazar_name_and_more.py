# Generated by Django 5.0.6 on 2025-01-04 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0005_alter_deposit_date_alter_fund_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fund',
            name='description',
        ),
        migrations.AlterField(
            model_name='bazar',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Salary',
        ),
    ]
