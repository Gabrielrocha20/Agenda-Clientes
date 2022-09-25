from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from pyexpat import model

from .models import Agenda, Categoria


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
            return render(request, 'agenda/pages/index.html')

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
            return render(request, 'agenda/pages/index.html')

    def post(self, request):
        client   = request.POST.get('client')
        time     = request.POST.get('time')
        date     = request.POST.get('date')
        category = request.POST.get('category')
        concluido = request.POST.get('verificados')
        pesquisar = request.POST.get('btn-pesquisar')
        if concluido is None:
            concluido = pesquisar.split(' ')[1]
            if concluido == 'on':
                classe = 'verificados_on'
            else:
                classe = 'verificados_off'
        if not pesquisar is None:
            if pesquisar.split(' ')[0]  == 'on':
                conclu = True if concluido == 'on' else False
                print(category)
                print(date)
                print(time)
                print(conclu)
                if category == '':
                    filtrar = Agenda.objects.filter(usuario = request.user, cliente__icontains = client, horario__icontains = time, data__icontains = date, concluido = conclu).order_by('-id')
                else:
                    filtrar = Agenda.objects.filter(usuario = request.user, servico__id =category, cliente__icontains = client, horario__icontains = time, data__icontains = date, concluido = conclu).order_by('-id')
                
                category = 'Serviço'

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
        category_id = ''
        if category != '':
            category = Categoria.objects.filter(id=category).first()
            category_id = category.id
        else:
            category = 'Serviço'
        
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
            'category_id': category_id
        })

        if category == '':
            filtro = Agenda.objects.filter(usuario = request.user, categoria__id = category, client__icontains = client, horario__icontains = time, data__icontains = date, concluido = concluido)
