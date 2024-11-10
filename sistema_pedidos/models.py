from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Mesa(models.Model):
    """Modelo que representa una mesa en el restaurante."""
    numero = models.PositiveIntegerField(unique=True)  # Número de la mesa, debe ser único
    disponible = models.BooleanField(default=True)  # Indica si la mesa está disponible
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # Relación con el usuario, campo nullable inicialmente

    def __str__(self):
        """Representación en cadena de la mesa."""
        return f"Mesa {self.numero} - {'Disponible' if self.disponible else 'No Disponible'}"

class Producto(models.Model):
    """Modelo que representa un producto del menú."""
    nombre = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField(blank=True, null=True)  # Descripción del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    
    categoria = models.CharField(max_length=50, choices=[  # Categoría del producto
        ('bebidas', 'Bebidas'),
        ('postres', 'Postres'),
        ('platos', 'Platos')
    ])
    
    stock = models.PositiveIntegerField(default=0)  # Stock disponible del producto

    def __str__(self):
        """Representación en cadena del producto."""
        return self.nombre

class Pedido(models.Model):
    """Modelo que representa un pedido realizado por una mesa."""
    ESTADO_PEDIDO = [  # Opciones de estado del pedido
        ('no tomado', 'No tomado'),
        ('en preparacion', 'En preparación'),
        ('servido', 'Servido')
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)  # Relación con la mesa
    estado = models.CharField(max_length=20, choices=ESTADO_PEDIDO, default='no tomado')  # Estado del pedido
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Relación con el usuario que hizo el pedido
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha de creación del pedido

    def __str__(self):
        """Representación en cadena del pedido."""
        return f"Pedido {self.id} en {self.mesa} por {self.usuario.username if self.usuario else 'Usuario no asignado'}"

class DetallePedido(models.Model):
    """Modelo que representa los detalles de un pedido."""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # Relación con el pedido
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)  # Relación con el producto
    cantidad = models.PositiveIntegerField()  # Cantidad del producto en el pedido
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Precio por unidad o total

    def __str__(self):
        """Representación en cadena del detalle del pedido."""
        return f"{self.cantidad} x {self.producto.nombre} en {self.pedido}"
