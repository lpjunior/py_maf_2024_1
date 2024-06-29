import hashlib
from django.shortcuts import render, redirect
from .models import Usuario, Contato
from .forms import UsuarioForm, ContatoForm, LoginForm
from django.db.models import Count


def registro(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest()
            usuario.save()
            return redirect('login')
        else:
            return render(request, 'usuarios/registro.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/registro.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            hashed_password = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            try:
                usuario = Usuario.objects.get(email=email, senha=hashed_password)
                request.session['usuario_id'] = usuario.id
                return redirect('dashboard')
            except Usuario.DoesNotExist:
                form.add_error(None, 'Email ou senha incorretos.')

    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})


def adicionar_contato(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
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
    else:
        return redirect('login')


def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.filter(id=usuario_id)
        contatos = Contato.objects.filter(usuario=usuario)
        return render(request, 'contatos/dashboard.html', {'usuario': usuario, 'contatos': contatos})
    else:
        return redirect('login')


def listar_usuarios(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuarios = Usuario.objects.annotate(num_contatos=Count('contatos'))
        return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})
    else:
        return redirect('login')


def logout(request):
    request.session.flush()
    return redirect('login')
