# Generated by Django 5.0.3 on 2025-03-04 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loan',
            name='loan_id',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='monthly_installment',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='total_interest',
        ),
        migrations.AlterField(
            model_name='loan',
            name='interest_rate',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='loan',
            name='status',
            field=models.CharField(default='ACTIVE', max_length=10),
        ),
        migrations.DeleteModel(
            name='PaymentSchedule',
        ),
    ]
