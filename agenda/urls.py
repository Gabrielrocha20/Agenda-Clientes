from django.urls import path
from . import views
app_name = 'agenda'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('consulta/', views.ConsultaView.as_view(), name='consulta'),
    path('cliente/<int:id>', views.ClienteView.as_view(), name='cliente'),
    path('conta/<int:id>', views.ContaView.as_view(), name='conta'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('editarCliente/<int:id>', views.EditarClienteView.as_view(), name='editarCliente'),
]
