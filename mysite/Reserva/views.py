from django.shortcuts import render, get_object_or_404, redirect, redirect
from django.contrib import messages
from .models import *
import locale
from datetime import datetime, timedelta
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.http import JsonResponse
import json
from .utils import formatar_data
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def index(request):
    if request.user.is_authenticated:
        return redirect('buscar_espacos')  # Altere para a URL que você quer redirecionar
    return render(request, 'reserva/index.html')

def teste(request):
    return render(request, 'reserva/visualizar_informacoes_espaco_esportivo.html')

def visualizar_informacoes_espaco_esportivo(request, espaco_id):
    # Recupera o espaço esportivo com o id fornecido
    espaco = get_object_or_404(EspacoEsportivo, id=espaco_id)
    
    # Recupera todos os recursos associados a esse espaço
    recursos = espaco.recurso.all()
    
    # Passa os dados para o template
    context = {
        'espaco': espaco,
        'recursos': recursos,
    }
    
    return render(request, 'reserva/visualizar_informacoes_espaco_esportivo.html', context)

def dashboard(request):
    return render(request, 'reserva/dashboard.html')

class EspacoEsportivoView(DetailView):
    model = EspacoEsportivo
    template_name = "reserva/visualizar_informacoes_espaco_esportivo.html"
    context_object_name = "espaco"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # O objeto espaco já está disponível como self.object
        espaco = self.object
        
        # Recupera todas as reservas relacionadas a esse espaço
        reservas = Reserva.objects.filter(agenda__recurso__espaco=espaco)
        
        # Recupera todos os recursos associados ao espaço esportivo
        recursos = espaco.recurso.all()
        
        # Adiciona as reservas e recursos ao contexto
        context['reservas'] = reservas
        context['recursos'] = recursos
        
        return context

def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    
    # Verifica se a reserva ainda não está cancelada
    if reserva.status != "cancelada":
        # Altera o status da reserva para 'cancelada'
        reserva.status = "cancelada"
        
        # Altera o status da agenda para 'Ativo'
        reserva.agenda.status = "ativo"
        
        # Salva a alteração na agenda
        reserva.agenda.save()

        # Salva a alteração na reserva
        reserva.save()

        # Mensagem de sucesso
        messages.success(request, "Reserva cancelada com sucesso.")
    else:
        # Mensagem de erro caso a reserva já esteja cancelada
        messages.error(request, "Esta reserva já está cancelada.")
    
    # Redireciona para a página de visualização da agenda
    return redirect('agenda')

class VisualizarAgendaView(ListView):
    model = Reserva  # Mostra a lista de reservas
    template_name = "reserva/visualizar_agenda_recurso.html"  # Template a ser renderizado
    context_object_name = "reservas"  # Nome do objeto no template

    def get_queryset(self):
        # Agora retorna todas as reservas sem filtrar por 'recurso_id'
        return Reserva.objects.select_related('organizador', 'agenda')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retira o 'recurso' do contexto, pois não estamos mais filtrando por 'recurso_id'
        context['recurso'] = None  # Se desejar exibir alguma informação relacionada ao recurso
        return context

class VisualizarAgendaRecursoView(ListView):
    model = Reserva  # Mostra a lista de reservas
    template_name = "reserva/visualizar_agenda_recurso.html"  # Template a ser renderizado
    context_object_name = "reservas"  # Nome do objeto no template

    def get_queryset(self): #O get_queryset é responsável por definir quais objetos serão passados para o template.
        recurso_id = self.kwargs['recurso_id']
        recurso = get_object_or_404(Recurso, id=recurso_id)
        return Reserva.objects.filter(agenda__recurso=recurso).select_related('organizador', 'agenda')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recurso_id = self.kwargs['recurso_id']
        context['recurso'] = get_object_or_404(Recurso, id=recurso_id)
        return context

def checkout(request, recurso_id):
    recurso = get_object_or_404(Recurso, id=recurso_id)

    # Corrigido: agora filtramos pelo campo correto `agenda__recurso`
    reservas = Reserva.objects.filter(agenda__recurso=recurso, status="confirmada").select_related('organizador', 'agenda')
    checkouts = Reserva.objects.filter(agenda__recurso=recurso, status="checkout").select_related('organizador', 'agenda')  # Filtro por 'checkout'
    concluidos = Reserva.objects.filter(agenda__recurso=recurso, status="concluido").select_related('organizador', 'agenda')  # Filtro por 'concluido'

    visualizar = {
        "recurso": recurso,
        "reservas": reservas,
        "checkouts": checkouts,
        "concluidos": concluidos,
    }
    return render(request, "reserva/checkout_recurso.html", visualizar)

class BuscarEspacoEsportivoView():

    def buscar_espacos(request):
        query = request.GET.get('query', '')  # Pegamos o texto da pesquisa
        uf = request.GET.get('uf', '')  # Pegamos a UF selecionada

        # Iniciamos a busca pegando todos os espaços
        espacos = EspacoEsportivo.objects.all()
        print(espacos)  # Verifique o que está sendo passado
        # Se houver um texto na busca (query)
        if query:
            # Filtra espaços que contenham o texto no nome ou na cidade (usando o Q para OR)
            espacos = espacos.filter(
                Q(nome__icontains=query) | Q(cidade__icontains=query)
            )

        # Se houver uma UF selecionada
        if uf:
            # Filtra os espaços pela UF selecionada (nota que no modelo é 'UF' com letras maiúsculas)
            espacos = espacos.filter(UF=uf)

        print(espacos)  # Verifique o que está sendo passado
        return render(request, 'reserva/buscar_espaco_esportivo.html', {'espacos': espacos})

class RealizarReservaView():
    
    def listAgendas(request, id):
        #print(request.user)
        # Define o locale para o português
        # locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
        
        calendario = []
        hoje = datetime.today()
        
        for i in range(10):  # Isso vai de 0 a 5, ou seja, 6 dias (hoje + 5 próximos)
            dia = hoje + timedelta(days=i)
            calendario.append({
                'data' : dia,
                'dia_semana': dia.strftime('%a').upper(),  # Abreviação do dia da semana em maiúsculas
                'dia_formatado': dia.strftime('%d/%m')     # Data no formato DD/MM
            })

        # Passa a lista 'calendario' para o template
        return render(request, "reserva/realizar_reserva_recurso.html", {
            'calendario': calendario,
            'recurso' : id,
        })
    
    
    
    def get_horarios_por_dia(request, recurso_id, dia_recurso):
        # Buscar o recurso
        recurso = get_object_or_404(Recurso, id=recurso_id)

        dia_recurso = datetime.strptime(dia_recurso, '%Y-%m-%d').date()
        # Filtrar os horários disponíveis para a data selecionada
        horarios = Agenda.objects.filter(recurso=recurso, dia=dia_recurso, status='ativo').order_by("h_inicial")

        # Formatar os dados para JSON
        horarios_data = [
            {
                "id": horario.id,
                "h_inicial": horario.h_inicial.strftime("%H:%M"),
                "h_final": horario.h_final.strftime("%H:%M"),
                "preco": str(horario.preco)
            }
            for horario in horarios
        ]

        return JsonResponse({"horarios": horarios_data})
    
    def get_horario_info(request, horario_id):
        try:
            # Buscar o Horário
            horario = Agenda.objects.get(id=horario_id)
            
            # Formatar a data
            data_formatada = formatar_data(horario.dia.strftime('%Y-%m-%d'))
            
            # Obter o período do dia (Manhã, Tarde, Noite)
            #periodo = periodo_do_dia(horario.h_inicial.hour)
            
            # Formatar o horário (exemplo: "Manhã, 07h às 08h")
            horario_formatado = f"{horario.h_inicial.strftime('%H')}h às {horario.h_final.strftime('%H')}h"
            
            # Obter a localização
            recurso = horario.recurso
            espaco = recurso.espaco
            localizacao = f"{espaco.nome}, {espaco.cidade}/{espaco.UF}"

            # Preço do horário
            preco_formatado = f"R$ {horario.preco:.2f}"

            # Retornar os dados no formato desejado
            return JsonResponse({
                "recurso": recurso.nome,
                "data": data_formatada,
                "horario": horario_formatado,
                "localizacao": localizacao,
                "preco": preco_formatado
            })

        except Agenda.DoesNotExist:
            return JsonResponse({"error": "Horário não encontrado"}, status=404)
        
    @login_required
    def set_reserva(request, horarioID):
        # Recupera o objeto Agenda com o id fornecido
        horario = get_object_or_404(Agenda, id=horarioID)

        # Verifica se o status do horário é 'ativo'
        if horario.status == 'ativo':
            try:
                # Obtém o Organizador associado ao usuário logado
                organizador = request.user.organizador
            except Organizador.DoesNotExist:
                # Caso o usuário não tenha um Organizador associado
                return HttpResponse("Você precisa ser um organizador para fazer uma reserva.")

            # Cria um novo objeto Reserva
            reserva = Reserva.objects.create(
                organizador=organizador,  # Atribui a instância de Organizador ao campo organizador
                agenda=horario,          # A reserva está associada ao horário
                status='reservado'         # Status inicial como 'pendente'
            )
            
            # Atualiza o status do horário para 'inativo'
            horario.status = 'inativo'
            horario.save()

            # Após criar a reserva e atualizar o status do horário, redireciona o usuário para uma página de confirmação
            return redirect('reservas')
        
        else:
            return HttpResponse("Este horário não está mais disponível para reserva (inativo).")
        

@login_required(login_url='login')  # 'login' é o nome da URL de login
def reservas_view(request):
    try:
        # Obtém o organizador associado ao usuário logado
        organizador = Organizador.objects.get(user=request.user)
    except Organizador.DoesNotExist:
        return redirect('login')  # Redireciona para o login caso o organizador não exista

    # Filtra as reservas por status para o organizador logado
    reservas_ativas = Reserva.objects.filter(organizador=organizador, status="reservado")
    reservas_concluidas = Reserva.objects.filter(organizador=organizador, status="concluida")

    # Passa as reservas para o template
    context = {
        'reservas_ativas': reservas_ativas,
        'reservas_concluidas': reservas_concluidas,
    }
    return render(request, 'reserva/avaliar_recurso.html', context)


