# Generated by Django 4.0.2 on 2022-02-19 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_alter_order_deliverer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deliverer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.deliverer'),
        ),
    ]
