from django.urls import path
from .views import index, login_user, logout_user, obtener_productos, crear_pedido, obtener_pedidos

urlpatterns = [
    path('index/', index, name='index'),
    path('login/', login_user, name='login'),  # Esta URL debe manejar tanto las peticiones normales como las de API
    path('logout/', logout_user, name='logout'),
    path('api/login/', login_user, name='login_api'),  # Añadir el endpoint de la API para el login
    path('api/products/all/', obtener_productos, name='obtener_productos'),
    path('api/pedido/', crear_pedido, name='crear_pedido'),
    path('api/pedidos/', obtener_pedidos, name='obtener_pedidos'),
]
