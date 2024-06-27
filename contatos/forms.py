from django import forms

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
        fields = ['nome', 'idade', 'email', 'senha']
        widgets = {
            'senha': forms.PasswordInput(),
        }


class ContatoForm(BootstrapModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'email', 'telefone', 'endereco']
        widgets = {
            'telefone': forms.TextInput(attrs={'data-mask': '(0000000000000'}),
            'endereco': forms.Textarea(attrs={'rows': 3}),
        }


class LoginForm(BootstrapModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'senha']
        widgets = {
            'senha': forms.PasswordInput(),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['placeholder'] = 'exemplo@dominio.com'
            self.fields['senha'].widget.attrs['placeholder'] = 'Sua senha'

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get('email')
            senha = cleaned_data.get('senha')

            if email and senha:
                try:
                    user = Usuario.objects.get(email=email)
                    if not user.check_password(senha):
                        raise forms.ValidationError('Senha incorreta.')
                except Usuario.DoesNotExist:
                    raise forms.ValidationError('Email não encontrado.')

            return cleaned_data
