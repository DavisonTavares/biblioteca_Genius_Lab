# usuarios/forms.py
import re
from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar Senha')

    class Meta:
        model = Usuario
        fields = ['username', 'nome_completo', 'email', 'password', 'tipo_usuario', 'endereco', 'telefone']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and not email.endswith("@gmail.com"):
            raise forms.ValidationError("O email deve ser do domínio @gmail.com.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            if len(password) < 8:
                raise forms.ValidationError("A senha deve ter pelo menos 8 caracteres.")
            if not re.search(r"[A-Z]", password):
                raise forms.ValidationError("A senha deve conter pelo menos uma letra maiúscula.")
            if not re.search(r"[a-z]", password):
                raise forms.ValidationError("A senha deve conter pelo menos uma letra minúscula.")
            if not re.search(r"[0-9]", password):
                raise forms.ValidationError("A senha deve conter pelo menos um número.")
            # Adicionar validação para caracteres especiais (opcional, mas recomendado)
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                raise forms.ValidationError("A senha deve conter pelo menos um caractere especial.")
            # Evitar senhas muito fracas, como '12345678' ou 'password'
            if re.match(r"^\d{8}$", password) or password.lower() in ['password', '12345678']:
                raise forms.ValidationError("A senha não pode ser uma sequência simples ou fraca.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("As senhas não correspondem.")
