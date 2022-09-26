from django.urls import path
from . import views
app_name = 'agenda'

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('consulta/', views.ConsultaView.as_view(), name='consulta'),
    path('cliente/', views.ClienteView.as_view(), name='cliente'),
    path('conta/', views.ContaView.as_view(), name='conta'),
]
