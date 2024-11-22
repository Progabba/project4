from django import forms
from .models import Recipient, Message, Mailing


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["email", "full_name", "comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']  # Укажите поля из модели Message
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите тему сообщения',
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст сообщения',
                'rows': 5,
            }),
        }
        labels = {
            'subject': 'Тема',
            'body': 'Текст сообщения',

        }

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
            }),
            'message': forms.Select(attrs={
                'class': 'form-control',
            }),
            'recipients': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'start_time': 'Дата и время начала',
            'end_time': 'Дата и время окончания',
            'status': 'Статус',
            'message': 'Сообщение',
            'recipients': 'Получатели',
        }