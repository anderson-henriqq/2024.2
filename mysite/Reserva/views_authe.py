from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrganizadorForm
from .models import Organizador
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib import messages
from .models import Organizador, Gerente

def user_login(request):
    # Verifique se o usuário já está logado
    if request.user.is_authenticated:
        # Checar se o usuário é um organizador ou gerente
        try:
            organizador = Organizador.objects.get(user=request.user)
            return redirect('buscar_espacos')  # Redireciona para a URL do organizador
        except Organizador.DoesNotExist:
            try:
                gerente = Gerente.objects.get(user=request.user)
                return redirect('home_gerente')  # Redireciona para a URL do gerente
            except Gerente.DoesNotExist:
                # Se o usuário não for nem organizador nem gerente, redireciona para a página inicial ou outro lugar
                return redirect('home')  # Alterar conforme sua necessidade

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Aqui, usamos o authenticate para validar o nome de usuário e a senha
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Se o usuário for autenticado, fazemos login
            login(request, user)
            
            # Checar o tipo de usuário após o login
            try:
                organizador = Organizador.objects.get(user=user)
                return redirect('buscar_espacos')  # Redireciona para a URL do organizador
            except Organizador.DoesNotExist:
                try:
                    gerente = Gerente.objects.get(user=user)
                    return redirect('home_gerente')  # Redireciona para a URL do gerente
                except Gerente.DoesNotExist:
                    # Se o usuário não for nem organizador nem gerente, redireciona para a página inicial ou outro lugar
                    return redirect('home')  # Alterar conforme sua necessidade
        else:
            # Se a autenticação falhar, exibe mensagem de erro
            messages.error(request, 'Nome de usuário ou senha inválidos.')

    return render(request, 'registration/login.html')  # Retorna o template de login


def user_logout(request):
    logout(request)  # Faz o logout do usuário
    return redirect('login')  # Redireciona para a página de login após o logout

def cadastrar_organizadores(request):
    if request.user.is_authenticated:
        return redirect('buscar_espacos')  
    
    if request.method == 'POST':
        form = OrganizadorForm(request.POST)

        if form.is_valid():
            # O form.save() agora salva tanto o User quanto o Organizador
            user = form.save()

            # Logando o usuário automaticamente
            login(request, user)
            
            # Mensagem de sucesso
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('buscar_espacos')  # Substitua 'home' com a URL da sua aplicação

        else:
            print("Formulário inválido:", form.errors)
            messages.error(request, 'Há erros no formulário. Por favor, verifique.')

    else:
        form = OrganizadorForm()

    return render(request, 'registration/signup.html', {'form': form})
