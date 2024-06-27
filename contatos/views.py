import hashlib
from django.shortcuts import render, redirect
from .models import Usuario, Contato
from .forms import UsuarioForm, ContatoForm, LoginForm


def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest()
            usuario.save()
            return redirect('login')
        else:
            return render(request, 'contatos/registro.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'contatos/registro.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = hashlib.sha256(form.cleaned_data['senha'].encode('utf-8')).hexdigest()

            try:
                usuario = Usuario.objects.get(email=email, senha=senha)
                request.session['usuario_id'] = usuario.id
                return redirect('dashboard')
            except Usuario.DoesNotExist:
                form.add_error(None, 'Email ou senha incorretos.')
        else:
            return render(request, 'contatos/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'contatos/login.html', {'form': form})


def adicionar_contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            contato = form.save(commit=False)
            contato.usuario_id = request.session.get('usuario_id')
            contato.save()
            return redirect('dashboard')
        else:
            return render(request, 'contatos/adicionar_contato.html', {'form': form})
    else:
        form = ContatoForm()
    return render(request, 'contatos/adicionar_contato.html', {'form': form})
