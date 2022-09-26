from importlib.metadata import requires
from pyexpat import model
import re
from urllib import request
from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Agenda, Categoria
from django.http import Http404



# views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'agenda/pages/index.html')

    def post(self, request):
        username = request.POST.get('userLog')
        password = request.POST.get('senhaLog')

        user = authenticate(username = username, password = password)

        if user:
            login(request, user = user)

            return redirect('agenda:registro')
        
        return redirect('agenda:login')



class RegistroView(View):


    def get(self, request):
        agenda = Agenda.objects.all().order_by('-id')
        categoria = Categoria.objects.all().order_by('-id')

        if request.user.is_authenticated:
            return render(request, 'agenda/pages/registro.html', context = {
                'agenda':agenda,
                'categorias':categoria
            })
        else:
            return redirect('agenda:login')

    def post(self, request):
        client   = request.POST.get('client')
        time     = request.POST.get('time')
        date     = request.POST.get('date')
        category = request.POST.get('category')
        description = request.POST.get('description')
        valor    = request.POST.get('valor')

        if (len(client) == 0) or (len(time) == 0) or (len(date) == 0) or (len(category) == 0) or (len(description) == 0) or (len(valor) == 0):
            raise Http404('deu ruim!')

        novoCadastro = Agenda.objects.create(usuario = request.user, cliente = client, horario = time, data = date, descricao = description, concluido = False, servico = Categoria.objects.get(categoria = category), valor = valor)

        novoCadastro.save()
        
        return redirect('agenda:registro')



class ConsultaView(View):

    def get(self, request):
        if request.user.is_authenticated:
            agenda = Agenda.objects.filter(usuario=request.user, concluido=False).order_by('-id')
            categoria = Categoria.objects.all().order_by('-id')

            return render(request, 'agenda/pages/consulta.html', context = {
                'agenda':agenda,
                'categorias':categoria,
                'category':'Serviço'
            })
        else:
            return redirect('agenda:login')

    def post(self, request):
        client   = request.POST.get('client')
        time     = request.POST.get('time')
        date     = request.POST.get('date')
        category = request.POST.get('category')
        concluido = request.POST.get('verificados')
        pesquisar = request.POST.get('btn-pesquisar')

        if pesquisar  == 'on':

            concluido = True if concluido == 'on' else False

            filtro = {
                '0':Agenda.objects.filter(usuario = request.user, categoria__id = category, client__icontains = client, horario__icontains = time, data__icontains = date, concluido = concluido),

                '1':Agenda.objects.filter(usuario = request.user, client__icontains = client, horario__icontains = time, data__icontains = date, concluido = concluido),
            }

            filtrar = filtro['0'] if not category is None else filtro['1']

            categoria = Categoria.objects.all().order_by('-id')
            return render(request, 'agenda/pages/consulta.html', context = {
                'agenda'    :filtrar,
                'categorias':categoria,
                'concluido' :concluido,
                'classe'    :classe,
                'client'    :client,
                'time'      :time,
                'date'      :date,
                'category'  :category,
            })



        if concluido == 'on':
            classe = 'verificados_on'
        else:
            classe = 'verificados_off'

        if category == '':
            category = 'Serviço'

        print(category)

        agenda = Agenda.objects.filter(usuario=request.user, concluido=False).order_by('-id')
        categoria = Categoria.objects.all().order_by('-id')

        return render(request, 'agenda/pages/consulta.html', context = {
            'agenda'    :agenda,
            'categorias':categoria,
            'concluido' :concluido,
            'classe'    :classe,
            'client'    :client,
            'time'      :time,
            'date'      :date,
            'category'  :category,
        })

        if category == '':
            filtro = Agenda.objects.filter(usuario = request.user, categoria__id = category, client__icontains = client, horario__icontains = time, data__icontains = date, concluido = concluido)



class ClienteView(View):
    def get(self, request, id):

        if request.user.is_authenticated:

            publicacao = Agenda.objects.filter(usuario = request.user, id = id)

            for cliente in publicacao:
                nome = cliente.cliente

            return render(request, 'agenda/pages/client.html',
            context = {
                'publicacao':publicacao,
                'nome':nome
            })
        else:
            return redirect('agenda:login')




class ContaView(View):
    def get(self, request):

        if request.user.is_authenticated:
            return render(request, 'agenda/pages/conta.html')
        else:
            return redirect('agenda:login')
