from django.contrib import admin
from .models import Categoria, Agenda

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    ...

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    ...