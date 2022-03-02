# Generated by Django 4.0.2 on 2022-02-28 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zomatoDemoAdmin', '0002_initial'),
        ('zomatoDemoCustomer', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='dishes',
        ),
        migrations.AddField(
            model_name='orders',
            name='order_dishes',
            field=models.ManyToManyField(related_name='cart_dishes', to='zomatoDemoAdmin.Dishes'),
        ),
    ]