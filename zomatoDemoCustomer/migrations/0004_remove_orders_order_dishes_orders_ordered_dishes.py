# Generated by Django 4.0.2 on 2022-02-28 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoDemoAdmin', '0002_initial'),
        ('zomatoDemoCustomer', '0003_remove_orders_dishes_orders_order_dishes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_dishes',
        ),
        migrations.AddField(
            model_name='orders',
            name='ordered_dishes',
            field=models.ManyToManyField(related_name='cart_dishes', through='zomatoDemoCustomer.Cart', to='zomatoDemoAdmin.Dishes'),
        ),
    ]
