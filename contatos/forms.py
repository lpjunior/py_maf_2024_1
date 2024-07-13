from django import forms
from django.contrib.auth import authenticate

from contatos.models import Usuario, Contato


class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class UsuarioForm(BootstrapModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario


class ContatoForm(BootstrapModelForm):
    foto = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*',
    }))

    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'logradouro', 'bairro', 'cidade', 'uf', 'cep', 'foto']
        widgets = {
            'telefone': forms.TextInput(attrs={'data-mask': '(00) 00000-0000'}),
            'cep': forms.TextInput(attrs={'data-mask': '00000-0000'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'exemplo@dominio.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Sua senha'
    }))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                usuario = authenticate(username=email, password=password)
                if usuario is None:
                    raise forms.ValidationError('Email ou senha incorretos ou usuário inativo.')
            except Usuario.DoesNotExist:
                raise forms.ValidationError('Email não encontrado.')

        return cleaned_data


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Sua senha atual'
    }))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nova senha'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirme a nova senha'
    }))

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            print('Confirmação de senha inválida')
            raise forms.ValidationError('Confirmação de senha inválida.')

        if new_password and old_password and new_password == old_password:
            print('A nova senha não pode ser igual à antiga.')
            raise forms.ValidationError('A nova senha não pode ser igual à antiga.')

        return cleaned_data
