from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Recipient
from .forms import RecipientForm

# Список клиентов
class RecipientListView(ListView):
    model = Recipient
    template_name = "recipients/recipient_list.html"
    context_object_name = "recipients"

# Создание клиента
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy('recipient_list')  # Используем reverse_lazy для отложенного реверса

# Редактирование клиента
class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipient_form.html"
    success_url = "/recipients/"

# Удаление клиента
class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipients/recipient_confirm_delete.html"
    success_url = "/recipients/"

