import hashlib

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models.usuarios import Usuario
from .usuarios.forms import UsuarioForm, LoginForm, CustomForm


def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        # valida se o formulário está preenchido corretamente
        if form.is_valid():
            # resgatando as informações vindas do formulário
            nome = form.cleaned_data.get('nome')
            idade = form.cleaned_data.get('idade')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')

            # criptografando a senha
            sha256_hash = hashlib.sha256()
            sha256_hash.update(senha.encode('utf-8'))
            senha_criptografada = sha256_hash.hexdigest()

            # persistindo na base usando o ORM
            Usuario.objects.create(nome=nome, idade=idade, email=email, senha=senha_criptografada)

            # Redireciona para a página de login
            return redirect('login')
        else:
            # Se o formulário é inválido, renderiza o template os erros
            return render(request, 'usuarios/registro.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # valida se o formulário está preenchido corretamente
        if form.is_valid():
            # resgatando as informações vindas do formulário
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')

            # criptografando a senha
            sha256_hash = hashlib.sha256()
            sha256_hash.update(senha.encode('utf-8'))
            senha_criptografada = sha256_hash.hexdigest()
            try:
                # Recupera os dados no banco
                usuario = Usuario.objects.get(email=email, senha=senha_criptografada)

                # Define a sessão 
                request.session['usuario_id'] = usuario.id

                # Redireciona
                return redirect('personalizar')
            except Usuario.DoesNotExist:
                return HttpResponse("Nome de usuário ou senha inválidos")
        else:
            # Se o formulário é inválido, renderiza o template os erros
            return render(request, 'usuarios/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def personalizar(request):
    if request.method == 'POST':
        form = CustomForm(request.POST)
        # valida se o formulário está preenchido corretamente
        if form.is_valid():
            cor_preferida = form.cleaned_data.get('cor_preferida')
            request.session['cor_preferida'] = cor_preferida
            response = redirect('dashboard')
            response.set_cookie('cor_preferida', cor_preferida, max_age=3600)
            return response
        else:
            return render(request, 'usuarios/personalizar.html', {'form': form})
    else:
        form = CustomForm()
    return render(request, 'usuarios/personalizar.html', {'form': form})


def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
    usuario = Usuario.objects.get(id=usuario_id)
    cor_preferida = request.COOKIES.get('cor_preferida', 'default')
    return render(request, 'usuarios/dashboard.html', {'usuario': usuario, 'cor_preferida': cor_preferida})


def logout(request):
    request.session.flush()
    response = redirect('login')
    response.delete_cookie('cor_preferida')
    return response
