# Generated by Django 4.1 on 2024-10-26 13:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mesa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(unique=True)),
                ('disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.CharField(choices=[('bebidas', 'Bebidas'), ('postres', 'Postres'), ('platos', 'Platos')], max_length=50)),
                ('stock', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('no tomado', 'No tomado'), ('en preparacion', 'En preparación'), ('servido', 'Servido')], default='no tomado', max_length=20)),
                ('fecha_pedido', models.DateTimeField(default=django.utils.timezone.now)),
                ('mesa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema_pedidos.mesa')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='sistema_pedidos.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema_pedidos.producto')),
            ],
        ),
    ]