# Generated by Django 4.2.9 on 2024-08-13 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luxmart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True)),
                ('discount_percentage', models.PositiveIntegerField()),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
    ]