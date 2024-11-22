from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    def __init__(self, *args, **kwargs):
        """Стилизация формы."""
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Единый CSS-класс для всех полей
                'placeholder': f'Введите {field.label.lower()}'
            })



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'phone_number', 'country']
    def __init__(self, *args, **kwargs):
        """Стилизация формы."""
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  # Единый CSS-класс для всех полей
                'placeholder': f'Введите {field.label.lower()}'
            })