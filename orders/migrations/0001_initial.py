# Generated by Django 5.1.7 on 2025-03-31 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField()),
                ('items', models.JSONField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('pending', 'В ожидании'), ('ready', 'Готово'), ('paid', 'Оплачено')], default='pending', max_length=10)),
            ],
        ),
    ]
