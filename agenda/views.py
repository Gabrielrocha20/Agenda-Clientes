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

        if request.user.is_authenticated:
            return redirect('agenda:conta', request.user.id)

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
                'categorias':categoria,
                'atualRegistro':True,
            })
        else:
            return redirect('agenda:login')

    def post(self, request):
        time     = request.POST.get('time')
        date     = request.POST.get('date')
        category = request.POST.get('category')
        description = request.POST.get('description')
        valor    = request.POST.get('valor')
        registraFiltro = request.POST.get('btn-confirma')

        print(registraFiltro)

        if registraFiltro == 'on':
            client   = request.POST.get('client').capitalize()
            
            if (len(client) == 0) or (len(time) == 0) or (len(date) == 0) or (len(category) == 0) or (len(description) == 0) or (len(valor) == 0):
                raise Http404('deu ruim!')

            novoCadastro = Agenda.objects.create(usuario = request.user, cliente = client, horario = time, data = date, descricao = description, concluido = False, servico = Categoria.objects.get(categoria = category), valor = valor)

            novoCadastro.save()
            
            return redirect('agenda:registro')
        
        categoria =  request.POST.get('novaCategoria')

        if  not categoria is None:
            novaCategoria = Categoria.objects.create(categoria = categoria)
            novaCategoria.save()
            print(categoria)
            
        return redirect('agenda:registro')



class ConsultaView(View):

    def get(self, request):
        if request.user.is_authenticated:
            agenda = Agenda.objects.filter(usuario=request.user, concluido=False).order_by('-id')
            categoria = Categoria.objects.all().order_by('-id')

            return render(request, 'agenda/pages/consulta.html', context = {
                'agenda':agenda,
                'categorias':categoria,
                'category':'Serviço',
                'atualConsulta':True,
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
                    'atualConsulta':True,
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
            'category_id': category_id,
            'atualConsulta':True,
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
                'nome':nome,
            })
        else:
            return redirect('agenda:login')




class ContaView(View):
    def get(self, request, id):

        if request.user.is_authenticated:
            publicacao = User.objects.filter(username = request.user, id = id)
            for user in publicacao:
                nome = user.username

            return render(request, 'agenda/pages/conta.html',
                context = {
                    'atualConta':True,
                    'nome':nome
                })
        else:
            return redirect('agenda:login')

    def post(self, request, id):

        sair    = request.POST.get('sair')
        salvar    = request.POST.get('salvar')

        if sair == 'on':
            return redirect('agenda:conta', id)

        print(sair, salvar)

        usuario = request.POST.get('username')
        senha   = request.POST.get('password')
        perfil  = User.objects.filter(username = request.user, id = id)

        for user in perfil:
                user.username = usuario
                user.set_password(senha)
                user.save()

        relog = authenticate(request, username = usuario, password = senha)
        login(request, user = relog)

        return redirect('agenda:conta', id)
            

class LogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)

        return redirect('agenda:login')


class EditarClienteView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            publicacao = Agenda.objects.filter(usuario = request.user, id = id)
            categorias = Categoria.objects.all()
            nome = publicacao[0].cliente
            return render(request, 'agenda/pages/editarCliente.html', context = {
                'publicacao':publicacao,
                'categorias':categorias,
                'nome':nome,
            })
        else:
            return redirect('agenda:login')

    def post(self, request, id):
        data      = request.POST.get('date')
        hora      = request.POST.get('time')
        categoria = request.POST.get('category')
        nome      = request.POST.get('client')
        valor     = request.POST.get('valor')
        descricao = request.POST.get('description')
        concluido = request.POST.get('concluido')
        print(concluido)
        concluido = False if concluido == None else True

        publicacao = Agenda.objects.filter(usuario=request.user, id=id)
        categorias = Categoria.objects.all().order_by('-id')

        print(data)
        for cliente in publicacao:
            cliente.cliente   = nome
            cliente.categoria = Categoria.objects.get(categoria=categoria)
            cliente.valor     = valor
            cliente.date      = data
            cliente.horario   = hora
            cliente.descricao = descricao
            cliente.concluido = concluido
            cliente.save()
        
        return redirect('agenda:editarCliente', id)

<<<<<<< HEAD




=======
>>>>>>> e01558be9b5875daf2ace8acaee06304da0b5556
class ExcluirClienteView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            publicacao = Agenda.objects.filter(usuario = request.user, id = id)
            publicacao.delete()
            return redirect('agenda:consulta')
        else:
<<<<<<< HEAD
            return redirect('agenda:login')
=======
            return redirect('agenda:login')
>>>>>>> e01558be9b5875daf2ace8acaee06304da0b5556
