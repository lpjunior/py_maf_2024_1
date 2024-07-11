import base64
import hashlib

from PIL import Image
import io

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Contato
from .forms import UsuarioForm, ContatoForm, LoginForm, PasswordChangeForm
from django.db.models import Count, Q
from django.utils.encoding import force_str
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token_utils import generate_token


def resend_activation_email(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    if usuario:
        if not usuario.is_active:
            send_activation_email(request, usuario)
            messages.success(request, 'O e-mail de ativação foi reenviado.')
        else:
            messages.info(request, 'Este usuário já está ativo.')
    return redirect('dashboard')


def send_activation_email(request, usuario):
    token = generate_token(usuario.pk)
    current_site = get_current_site(request)
    mail_subject = 'Ative sua conta'
    from_email = 'agenda.contato.senac@gmail.com'
    recipient_list = [usuario.email]
    message = render_to_string('usuarios/activation_email.html', {
        'user': usuario,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(usuario.id)),
        'token': token,
    })
    send_mail(mail_subject, '', from_email, recipient_list, fail_silently=False, html_message=message)
    usuario.token = token
    usuario.save()


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
            query = request.GET.get('q')
            status = request.GET.get('status')
            idade = request.GET.get('idade')
            usuarios = Usuario.objects.all()

            if query:
                usuarios = usuarios.filter(Q(nome__icontains=query) | Q(email__icontains=query))

            if status:
                is_active = True if status == 'ativo' else False
                usuarios = usuarios.filter(is_active=is_active)

            if idade:
                try:
                    idade = int(idade)
                    faixa_min = idade - 3
                    faixa_max = idade + 3
                    usuarios = usuarios.filter(idade__range=(faixa_min, faixa_max))

                    #  __gte(greater than or equal to): ele seleciona registros onde o valor do campo é maior ou igual a um valor especificado.
                    #  --range: ele seleciona registros onde o valor do campo está dentro de um intervalo especificado.
                except ValueError:
                    pass  # Se a idade não for um número, ignorar este filtro.

            usuarios = usuarios.filter(is_admin=False).annotate(contatos_count=Count('contatos'))
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
            usuario.password = hashlib.sha256(usuario.password.encode('utf-8')).hexdigest()
            usuario.save()
            send_activation_email(request, usuario)
            messages.success(request, 'Por favor, verifique seu email para ativar sua conta.')
            return redirect('login')
        else:
            return render(request, 'usuarios/adicionar_usuario.html', {'form': form})
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/adicionar_usuario.html', {'form': form})


def activate(request, uidb64, token):
    try:
        usuario_id = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.defer('password').get(pk=usuario_id)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None

    #if user is not None and default_token_generator.check_token(user, token):
    if usuario is not None and token == usuario.token:
        usuario.is_active = True
        usuario.token = ""
        usuario.save()
        messages.success(request, 'Conta ativada com sucesso. Você pode agora fazer login.')
        return redirect('login')
    else:
        messages.error(request, 'Link de ativação inválido.')
        return redirect('registro')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            hashed_password = hashlib.sha256(senha.encode('utf-8')).hexdigest()

            try:
                usuario = Usuario.objects.only('id', 'is_active').get(email=email, password=hashed_password)
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
            form = ContatoForm(request.POST, request.FILES)
            if form.is_valid():
                contato = form.save(commit=False)
                contato.usuario_id = request.session.get('usuario_id')

                if 'foto' in request.FILES:
                    imagem = Image.open(request.FILES['foto'])
                    imagem = imagem.resize((300, 300), Image.LANCZOS)
                    buffered = io.BytesIO()
                    imagem.save(buffered, format="PNG")
                    contato.foto_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

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
            form = ContatoForm(request.POST, request.FILES, instance=contato)
            if form.is_valid():
                contato = form.save(commit=False)

                if 'foto' in request.FILES:
                    imagem = Image.open(request.FILES['foto'])
                    imagem = imagem.resize((300, 300), Image.LANCZOS)
                    buffered = io.BytesIO()
                    imagem.save(buffered, format="PNG")
                    contato.foto_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                contato.save()

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
        query = request.GET.get('q')
        usuario = Usuario.objects.defer('password').get(
            id=usuario_id)  # defer() carrega todos os campos do modelo, exceto o(s) especificado(s)
        if usuario.is_admin:
            total_usuarios = Usuario.objects.filter(is_admin=False).count()
            usuarios_ativos = Usuario.objects.filter(is_admin=False, is_active=True).count()
            usuarios_inativos = total_usuarios - usuarios_ativos
            ultimos_usuarios = Usuario.objects.filter(is_admin=False).order_by('-created_at')[:5]

            context = {
                'usuario': usuario,
                'total_usuarios': total_usuarios,
                'usuarios_ativos': usuarios_ativos,
                'usuarios_inativos': usuarios_inativos,
                'ultimos_usuarios': ultimos_usuarios
            }
        else:
            contatos = Contato.objects.filter(usuario=usuario)

            if query:
                contatos = contatos.filter(
                    Q(nome__icontains=query) |
                    Q(email__icontains=query) |
                    Q(bairro__icontains=query) |
                    Q(cidade__icontains=query) |
                    Q(uf__icontains=query)
                )

            context = {
                'usuario': usuario,
                'contatos': contatos
            }
        return render(request, 'contatos/dashboard.html', context)
    else:
        return redirect('login')


def logout(request):
    request.session.flush()
    return redirect('login')


def change_password(request):
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        usuario = Usuario.objects.only('email').get(id=usuario_id)  # 'only()' carrega apenas o(s) campo(s) 
        # especificado(s)
        if request.method == 'POST':
            form = PasswordChangeForm(request.POST)
            try:
                if form.is_valid():
                    old_password = form.cleaned_data['old_password']
                    new_password = form.cleaned_data['new_password']
                    confirm_password = form.cleaned_data['confirm_password']

                    hashed_old_password = hashlib.sha256(old_password.encode('utf-8')).hexdigest()
                    hashed_new_password = hashlib.sha256(new_password.encode('utf-8')).hexdigest()

                    if usuario.password == hashed_old_password:
                        if new_password == confirm_password:
                            usuario.password = hashed_new_password
                            usuario.save()
                            messages.success(request, 'Senha alterada com sucesso!')
                            return redirect('dashboard')
                        else:
                            form.add_error(None, 'As senhas não coincidem.')
                    else:
                        form.add_error(None, 'Senha antiga incorreta')
            except form.ValidationError:
                form.add_error(None, 'Corrija os erros.')
        else:
            form = PasswordChangeForm()
        return render(request, 'usuarios/change_password.html', {'form': form})
    else:
        return redirect('login')
