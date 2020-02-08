# Generated by Django 3.1.dev20200113081333 on 2020-01-23 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Extras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extrasName', models.CharField(max_length=64, verbose_name='Extras Name')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categoryName', models.CharField(max_length=64, verbose_name='Category Name')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itemName', models.CharField(max_length=64)),
                ('priceSmall', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('priceLarge', models.DecimalField(decimal_places=2, max_digits=5)),
                ('extrasAllowed', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemcategory', to='pizza.ItemCategory')),
                ('extras', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemextras', to='pizza.Extras')),
            ],
        ),
        migrations.CreateModel(
            name='SubsExtra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Toppings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=24)),
                ('password', models.CharField(max_length=24)),
                ('name', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=64)),
                ('contactNumber', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalAmount', models.FloatField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userOrder', to='pizza.Users')),
            ],
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(choices=[('S', 'Small'), ('L', 'Large')], default='L', max_length=1)),
                ('quantity', models.IntegerField(default=1)),
                ('menuId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menuID', to='pizza.Menu')),
                ('orderId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderID', to='pizza.Orders')),
                ('toppingsId', models.ManyToManyField(blank=True, related_name='toppingsID', to='pizza.Toppings')),
            ],
        ),
    ]