# Generated by Django 5.0.3 on 2025-03-06 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0004_remove_loan_is_foreclosed_loan_collateral_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='loan_id',
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
