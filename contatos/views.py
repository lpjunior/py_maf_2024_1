import hashlib
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Contato
from .forms import UsuarioForm, ContatoForm, LoginForm
from django.db.models import Count

from django.contrib.auth.decorators import user_passes_test, login_required

from django.contrib.auth import authenticate, login as auth_login

from django.contrib import messages


# views para admin
#def is_admin(user):
#    return user.is_authenticated and user.is_admin


#@login_required
#@user_passes_test(is_admin)
def listar_usuarios(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        if usuario.is_admin:
            usuarios = Usuario.objects.filter(is_admin=False).annotate(num_contatos=Count('contatos'))
            return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})
        else:
            messages.error(request, 'Você não tem permissão para acessar essa página.')
            return redirect('dashboard')
    else:
        return redirect('login')


#@login_required
#@user_passes_test(is_admin)
def desativar_usuario(request, usuario_id):
    try:
        #usuario_logado = request.user
        usuario_logado_id = request.session.get('usuario_id')
        usuario_logado = Usuario.objects.get(id=usuario_logado_id)
        if usuario_logado:
            usuario_a_desativar = get_object_or_404(Usuario, id=usuario_id)
            if usuario_logado.is_admin:
                usuario_a_desativar.is_active = False
                usuario_a_desativar.save()
                messages.success(request, f'Usuário \'{usuario_a_desativar.nome}\' desativado com sucesso.')
            else:
                messages.error(request, 'Você não tem permissão para desativar usuários.')
                return redirect('dashboard')
            return redirect('listar_usuarios')
        else:
            return redirect('login')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')


#@login_required
#@user_passes_test(is_admin)
def reativar_usuario(request, usuario_id):
    try:
        #usuario_logado = request.user
        usuario_logado_id = request.session.get('usuario_id')
        usuario_logado = Usuario.objects.get(id=usuario_logado_id)
        if usuario_logado:
            usuario_a_reativar = get_object_or_404(Usuario, id=usuario_id)
            if usuario_logado.is_admin:
                usuario_a_reativar.is_active = True
                usuario_a_reativar.save()
                messages.success(request, f'Usuário \'{usuario_a_reativar.nome}\' reativado com sucesso.')
            else:
                messages.error(request, 'Você não tem permissão para reativar usuários.', extra_tags='danger')
                return redirect('dashboard')
            return redirect('listar_usuarios')
        else:
            return redirect('login')
    except Usuario.DoesNotExist:
        messages.error(request, 'Usuário não encontrado.')


#@login_required
#@user_passes_test(is_admin)
def excluir_usuario(request, usuario_id):
    #usuario_logado = request.user
    usuario_logado_id = request.session.get('usuario_id')
    usuario_logado = Usuario.objects.get(id=usuario_logado_id)
    if usuario_logado:
        usuario_a_ser_excluido = get_object_or_404(Usuario, id=usuario_id)
        if usuario_logado.is_admin:
            usuario_a_ser_excluido.delete()
            messages.success(request, f'Usuário \'{usuario_a_ser_excluido.nome}\' excluído com sucesso.')
        else:
            messages.error(request, 'Você não tem permissão para excluir usuários.')
        return redirect('listar_usuarios')
    else:
        return redirect('login')


# views para não admins
def adicionar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.senha = hashlib.sha256(usuario.senha.encode('utf-8')).hexdigest()
            usuario.save()
            return redirect('login')
        else:
            return render(request, 'usuarios/adicionar_usuario.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/adicionar_usuario.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            hashed_password = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            try:
                usuario = Usuario.objects.get(email=email, senha=hashed_password)
                # usuario = authenticate(request, username=email, password=hashed_password)
                if usuario is not None:
                    if usuario.is_active:
                        request.session['usuario_id'] = usuario.id
                        # auth_login(request, usuario)
                        return redirect('dashboard')
                    else:
                        form.add_error(None, 'Este usuário está desativado.')
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
                messages.success(request, f'Contato \'{contato.nome}\' adicionado com sucesso!')
                return redirect('dashboard')
            else:
                return render(request, 'contatos/adicionar_contato.html', {'form': form})
        else:
            form = ContatoForm()
        return render(request, 'contatos/adicionar_contato.html', {'form': form})
    else:
        return redirect('login')


def editar_contato(request, contato_id):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        contato = get_object_or_404(Contato, id=contato_id, usuario_id=usuario_id)
        if request.method == 'POST':
            form = ContatoForm(request.POST, instance=contato)
            if form.is_valid():
                form.save()
                messages.success(request, f'Contato \'{contato.nome}\' atualizado com sucesso!')
                return redirect('dashboard')

        form = ContatoForm(instance=contato)
        return render(request, 'contatos/editar_contato.html', {'form': form, 'contato': contato})
    else:
        return redirect('login')


def excluir_contato(request, contato_id):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        contato = get_object_or_404(Contato, id=contato_id, usuario_id=usuario_id)
        if request.method == 'POST':
            contato.delete()
            messages.success(request, f'Contato excluído com sucesso!')
            return redirect('dashboard')
        return render(request, 'contatos/excluir_contato.html', {'contato': contato})
    else:
        return redirect('login')


def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.get(id=usuario_id)
        contatos = Contato.objects.filter(usuario=usuario)
        return render(request, 'contatos/dashboard.html', {'usuario': usuario, 'contatos': contatos})
    else:
        return redirect('login')


def logout(request):
    request.session.flush()
    return redirect('login')
