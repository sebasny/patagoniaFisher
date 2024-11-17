import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Producto, Mesa, Pedido, DetallePedido


@login_required
def index(request):
    """Renderiza la página de inicio."""
    return render(request, 'index.html')



def login_user(request):
    """Maneja el inicio de sesión del usuario"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Intentamos autenticar al usuario
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirigir a la página de inicio
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'login.html')  # Redirige al formulario de login si GET o fallo en POST
def logout_user(request):
    """Cierra la sesión del usuario y redirige a la página de inicio de sesión."""
    logout(request)
    return redirect('login')


@require_http_methods(['GET'])
def obtener_productos(request):
    """Obtiene la lista de productos disponibles."""
    productos = Producto.objects.all().values('id', 'nombre', 'precio', 'categoria', 'stock')
    return JsonResponse({'products': list(productos)}, status=200)


@login_required
def mesa_detail(request, mesa_id):
    """Muestra los detalles de la mesa solo si el usuario es el propietario."""
    mesa = get_object_or_404(Mesa, id=mesa_id, usuario=request.user)
    return render(request, 'mesa_detail.html', {'mesa': mesa})


@require_http_methods(['POST'])
def crear_pedido(request):
    """Crea un nuevo pedido y reduce el stock de los productos."""
    data = json.loads(request.body)
    mesa_id = data.get('mesa_id')
    items = data.get('items')

    for item in items:
        producto_id = item['producto_id']
        cantidad = item['cantidad']

        producto = Producto.objects.get(id=producto_id)

        if producto.stock < cantidad:  # Verificar si hay suficiente stock
            return JsonResponse({'error': f'No hay suficiente stock para {producto.nombre}'}, status=400)

        # Si hay stock suficiente, crea el pedido y reduce el stock
        pedido = Pedido.objects.create(mesa_id=mesa_id)
        DetallePedido.objects.create(pedido=pedido, producto=producto, cantidad=cantidad, precio=producto.precio)

        # Reducir el stock
        producto.stock -= cantidad
        producto.save()

    return JsonResponse({'mensaje': 'Pedido creado con éxito!'}, status=201)


# @require_http_methods(['GET'])
# def obtener_pedidos(request):
#     """Obtiene la lista de pedidos realizados."""
#     pedidos = Pedido.objects.prefetch_related('detalles').all()
#     resultado = []

#     for pedido in pedidos:
#         detalles = [f"{detalle.cantidad} x {detalle.producto.nombre}" for detalle in pedido.detalles.all()]
#         resultado.append({
#             'id': pedido.id,
#             'mesa_id': pedido.mesa.id,
#             'estado': pedido.estado,
#             'fecha': pedido.fecha.strftime('%Y-%m-%d %H:%M:%S'),  # Formato de fecha
#             'detalles': ', '.join(detalles)  # Lista de detalles en una cadena
#         })

#     return JsonResponse({'pedidos': resultado}, status=200)


@require_http_methods(['GET'])
def obtener_pedidos(request):
    """Obtiene la lista de pedidos realizados con detalles individuales de cada producto."""
    pedidos = Pedido.objects.prefetch_related('detalles').all()
    resultado = []

    for pedido in pedidos:
        detalles = [
            {
                'producto_id': detalle.producto.id,
                'nombre': detalle.producto.nombre,
                'cantidad': detalle.cantidad,
                'precio': detalle.precio  # Precio del producto en el momento del pedido
            }
            for detalle in pedido.detalles.all()
        ]
        resultado.append({
            'id': pedido.id,
            'mesa_id': pedido.mesa.id if pedido.mesa else None,
            'estado': pedido.estado,
            'fecha': pedido.fecha.strftime('%Y-%m-%d %H:%M:%S'),
            'detalles': detalles
        })

    return JsonResponse({'pedidos': resultado}, status=200)