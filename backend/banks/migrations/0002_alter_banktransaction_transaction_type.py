# Generated by Django 5.0.14 on 2025-05-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banktransaction',
            name='transaction_type',
            field=models.CharField(blank=True, choices=[('credit', 'Credit'), ('debit', 'Debit')], default=None, max_length=6, null=True),
        ),
    ]
