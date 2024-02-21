# Generated by Django 5.0.1 on 2024-01-24 04:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItemlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productmaster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.userprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
