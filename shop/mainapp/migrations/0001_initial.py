# Generated by Django 3.1.4 on 2021-01-05 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='название')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True, verbose_name='название модели')),
                ('repair_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='цена ремонта')),
                ('sale_cost', models.DecimalField(blank=True, decimal_places=2, max_digits=11, null=True, verbose_name='цена продажи')),
                ('repaid_len', models.PositiveIntegerField(default=1, verbose_name='длительность ремонта в днях')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.brand', verbose_name='brand')),
            ],
        ),
    ]