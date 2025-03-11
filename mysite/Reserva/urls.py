from django.urls import path
from .views import RealizarReservaView, BuscarEspacoEsportivoView, EspacoEsportivoView, VisualizarAgendaView
from . import views, views_authe

urlpatterns = [

    path('', views.index, name='home'),
    path('login/', views_authe.user_login, name='login'),
    path('signup/', views_authe.cadastrar_organizadores, name='cadastro_organizador'),
    path('logout/', views_authe.user_logout, name='logout'),  # URL para o logout
    #path('visualizarAgenda/<int:recurso_id>/', views.visualizar_agenda, name='visualizar_agenda'),
    
    path('buscar/', BuscarEspacoEsportivoView.buscar_espacos, name='buscar_espacos'),
    path('EspacoEsportivo/<int:espaco_id>', views.visualizar_informacoes_espaco_esportivo, name='espaco'),
    path('Agenda/<int:id>', RealizarReservaView.listAgendas, name='realizar_reserva'),
    path("horarios/<int:recurso_id>/<str:dia_recurso>/", RealizarReservaView.get_horarios_por_dia, name="get_horarios"),
    path("getInfoAgenda/<int:horario_id>", RealizarReservaView.get_horario_info, name="getInfoAgenda"),
    path("setAgenda/<int:horarioID>", RealizarReservaView.set_reserva, name="setAgenda"),
    path('reservas/', views.reservas_view, name='reservas'),
    
    path('dashboard/' ,views.dashboard, name='home_gerente'),
    path('visualizarAgenda/' ,VisualizarAgendaView.as_view(), name='agenda'),
    path('checkout/<int:recurso_id>/', views.checkout, name='checkout'),

    path('cancelar_reserva/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]