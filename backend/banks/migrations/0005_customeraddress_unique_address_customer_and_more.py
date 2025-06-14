# Generated by Django 5.0.3 on 2025-06-10 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0004_alter_customerbvn_bvn_alter_customeremail_email_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='customeraddress',
            constraint=models.UniqueConstraint(fields=('address', 'customer'), name='unique_address_customer'),
        ),
        migrations.AddConstraint(
            model_name='customerbvn',
            constraint=models.UniqueConstraint(fields=('bvn', 'customer'), name='unique_bvn_customer'),
        ),
        migrations.AddConstraint(
            model_name='customeremail',
            constraint=models.UniqueConstraint(fields=('email', 'customer'), name='unique_email_customer'),
        ),
        migrations.AddConstraint(
            model_name='customermobile',
            constraint=models.UniqueConstraint(fields=('mobile', 'customer'), name='unique_mobile_customer'),
        ),
        migrations.AddConstraint(
            model_name='customername',
            constraint=models.UniqueConstraint(fields=('name', 'customer'), name='unique_name_customer'),
        ),
        migrations.AddConstraint(
            model_name='customernuban',
            constraint=models.UniqueConstraint(fields=('nuban', 'customer'), name='unique_nuban_customer'),
        ),
        migrations.AddConstraint(
            model_name='customerpassport',
            constraint=models.UniqueConstraint(fields=('passport', 'customer'), name='unique_passport_customer'),
        ),
        migrations.AddConstraint(
            model_name='customertin',
            constraint=models.UniqueConstraint(fields=('tin', 'customer'), name='unique_tin_customer'),
        ),
    ]
