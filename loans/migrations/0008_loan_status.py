# Generated by Django 5.0.3 on 2025-03-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0007_loan_amount_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('CLOSED', 'Closed')], default='ACTIVE', max_length=10),
        ),
    ]
