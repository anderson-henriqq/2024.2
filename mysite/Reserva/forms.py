from django import forms
from django.contrib.auth.models import User
from .models import Organizador
from django.core.exceptions import ValidationError

class OrganizadorForm(forms.ModelForm):
    nome = forms.CharField(max_length=64, label="Nome e Sobrenome")
    username = forms.CharField(max_length=150, label="Nome de Usuário")
    senha = forms.CharField(widget=forms.PasswordInput(), label="Senha")
    confirm_senha = forms.CharField(widget=forms.PasswordInput(), label="Confirme sua senha")

    class Meta:
        model = User
        fields = ['username', 'senha']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get('senha')
        confirm_senha = cleaned_data.get('confirm_senha')

        if senha != confirm_senha:
            raise ValidationError('As senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        # Criação do usuário
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['senha'])  # Processa a senha
        user.first_name = self.cleaned_data['nome']  # Adiciona o nome no campo first_name do User
        user.is_staff = False  # Garantir que o usuário não será admin

        # Salva o usuário primeiro
        if commit:
            user.save()

        # Criação do organizador depois que o usuário foi salvo
        organizador = Organizador(nome=self.cleaned_data['nome'], user=user)
        organizador.save()  # Salva o organizador no banco de dados

        return user  # Retorna o usuário criado
