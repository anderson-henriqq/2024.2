from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
from .models import Organizador, Gerente, EspacoEsportivo, Recurso, Agenda, Reserva

# Formulário para criar Organizador
class OrganizadorAdminForm(forms.ModelForm):
    class Meta:
        model = Organizador
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Se não for uma instância existente (novo Organizador)
            self.fields['user'].queryset = User.objects.filter(is_staff=True)  # Permitir que o Organizador seja associado a um usuário com permissão de staff

# Admin para Organizador
class OrganizadorAdmin(admin.ModelAdmin):
    form = OrganizadorAdminForm
    list_display = ('nome', 'user')  # Campos exibidos na listagem
    search_fields = ('nome',)

# Formulário para criar Gerente
class GerenteAdminForm(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:  # Se não for uma instância existente (novo Gerente)
            self.fields['user'].queryset = User.objects.filter(is_staff=True)  # Permitir que o Gerente seja associado a um usuário com permissão de staff

# Admin para Gerente
class GerenteAdmin(admin.ModelAdmin):
    form = GerenteAdminForm
    list_display = ('nome', 'cpf', 'user')  # Campos exibidos na listagem
    search_fields = ('nome', 'cpf')
    # list_filter = ('email',)  # Filtros disponíveis no painel de admin

# Admin para EspacoEsportivo
class EspacoEsportivoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'UF', 'gerente', 'media_avaliacao')
    search_fields = ('nome', 'cidade', 'UF')

# Definir uma classe de admin personalizada para o modelo Recurso
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('modalidade', 'get_espaco_nome')  # Usando um método para acessar o nome do espaco
    search_fields = ('modalidade', 'espaco__nome')  # Pesquisa pelo nome do espaco
    list_filter = ('modalidade',)  # Filtros disponíveis no painel de admin

    def get_espaco_nome(self, obj):
        return obj.espaco.nome  # Acessa o nome do EspacoEsportivo relacionado ao Recurso
    get_espaco_nome.admin_order_field = 'espaco__nome'  # Permite ordenar pela coluna 'nome' do EspacoEsportivo
    get_espaco_nome.short_description = 'Espaço'  # Título para a coluna na lista

# Admin para Agenda
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('preco', 'dia', 'h_inicial', 'h_final', 'recurso', 'status')
    search_fields = ('dia', 'h_inicial', 'h_final', 'recurso__nome')
    list_filter = ('dia', 'recurso')  # Filtros disponíveis no painel de admin

# Definir uma classe de admin personalizada para o modelo Reserva
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('organizador', 'agenda', 'status', 'criado_em')  # Campos que serão exibidos na lista
    search_fields = ('organizador__nome', 'horario__dia', 'status')  # Campos para pesquisa
    list_filter = ('status', 'organizador')  # Filtros disponíveis no painel de admin
    date_hierarchy = 'criado_em'  # Para filtrar por data

# Registro dos modelos no Admin
admin.site.register(Organizador, OrganizadorAdmin)
admin.site.register(Gerente, GerenteAdmin)
admin.site.register(EspacoEsportivo, EspacoEsportivoAdmin)
admin.site.register(Recurso, RecursoAdmin)
admin.site.register(Agenda, AgendaAdmin)
admin.site.register(Reserva, ReservaAdmin)
