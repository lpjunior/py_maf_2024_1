from django import forms
from ..models.usuarios import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'idade', 'email', 'senha']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Informe o nome'}),
            'senha': forms.PasswordInput(attrs={'class': 'form-control'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'min': 18}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@senac.rj'}),
        }


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'exemplo@senac.rj'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'senha'}))


class CustomForm(forms.Form):
    cor_preferida = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}))
