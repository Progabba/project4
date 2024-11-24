from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Recipient, Message, Mailing, MailingAttempt
from .forms import RecipientForm, MessageForm, CampaignForm
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime


# Список клиентов
class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "recipients/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        user = self.request.user
        # Менеджеры могут просматривать всех клиентов
        if user.groups.filter(name="менеджер").exists():
            return Recipient.objects.all()
        # Обычные пользователи могут видеть только своих клиентов
        return Recipient.objects.filter(user=user)

# Создание клиента
class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy('sendler:recipient_list')  # Используем reverse_lazy для отложенного реверса

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем клиента к текущему пользователю
        return super().form_valid(form)

# Редактирование клиента
class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy('sendler:recipient_list')  # Используем reverse_lazy для отложенного реверса

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        # Проверка, является ли пользователь владельцем продукта или администратором
        if recipient.user != request.user:
            return HttpResponseForbidden("У вас нет прав для редактирования этого получателя.")
        return super().dispatch(request, *args, **kwargs)

# Удаление клиента
class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "recipients/recipient_confirm_delete.html"
    success_url = reverse_lazy('sendler:recipient_list')  # Используем reverse_lazy для отложенного реверса

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        # Проверка, является ли пользователь владельцем продукта или администратором
        if recipient.user != request.user:
            return HttpResponseForbidden("У вас нет прав для удаления этого получателя.")
        return super().dispatch(request, *args, **kwargs)

# Список сообщений
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "messages/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        user = self.request.user
        # Менеджер может просматривать все рассылки
        if user.groups.filter(name="менеджер").exists():
            return Message.objects.all()
        # Обычные пользователи могут видеть только свои рассылки
        return Message.objects.filter(user=user)

# Создание сообщения
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/message_form.html"
    success_url = reverse_lazy('sendler:message_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  # Привязываем клиента к текущему пользователю
        return super().form_valid(form)

# Редактирование сообщения
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/message_form.html"
    success_url = reverse_lazy('sendler:message_list')

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        # Проверка, является ли пользователь владельцем продукта или администратором
        if recipient.user != request.user:
            return HttpResponseForbidden("У вас нет прав для редактирования этого сообщения.")
        return super().dispatch(request, *args, **kwargs)

# Удаление сообщения
class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "messages/message_confirm_delete.html"
    success_url = reverse_lazy('sendler:message_list')

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        # Проверка, является ли пользователь владельцем продукта или администратором
        if recipient.user != request.user:
            return HttpResponseForbidden("У вас нет прав для удаления этого сообщения.")
        return super().dispatch(request, *args, **kwargs)

# Список рассылок
class CampaignListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = "campaigns/campaign_list.html"
    context_object_name = "campaigns"

    def get_queryset(self):
        user = self.request.user
        # Менеджер может просматривать все рассылки
        if user.groups.filter(name="менеджер").exists():
            return Mailing.objects.all()
        # Обычные пользователи могут видеть только свои рассылки
        return Mailing.objects.filter(user=user)

# Создание рассылки
class CampaignCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy('sendler:campaign_list')

    def form_valid(self, form):
        # Устанавливаем поле user на текущего пользователя
        form.instance.user = self.request.user
        # Сохраняем объект с указанным пользователем
        return super().form_valid(form)

# Редактирование рассылки
class CampaignUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy('sendler:campaign_list')

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        # Проверка, является ли пользователь владельцем продукта или администратором
        if recipient.user != request.user:
            return HttpResponseForbidden("У вас нет прав для редактирования этой рассылки.")
        return super().dispatch(request, *args, **kwargs)

# Удаление рассылки
class CampaignDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = "campaigns/campaign_confirm_delete.html"
    success_url = reverse_lazy('sendler:campaign_list')

    def dispatch(self, request, *args, **kwargs):
        recipient = self.get_object()
        # Проверка, является ли пользователь владельцем продукта или администратором
        if recipient.user != request.user:
            return HttpResponseForbidden("У вас нет прав для удаления этой рассылки.")
        return super().dispatch(request, *args, **kwargs)

# Детали рассылки
class CampaignDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = "campaigns/campaign_detail.html"
    context_object_name = "campaign"


class SendMailingView(View):
    def post(self, request, *args, **kwargs):
        # Получаем рассылку по pk
        mailing = Mailing.objects.get(pk=kwargs['pk'])

        # Проверяем статус рассылки
        if mailing.status != "started":
            mailing.status = "started"
            mailing.save()

        # Отправляем сообщение каждому получателю
        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    mailing.message.subject,
                    mailing.message.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient.email],
                )
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="success",
                    server_response="Message sent successfully",
                    attempt_time=datetime.now()
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing,
                    status="failure",
                    server_response=str(e),
                    attempt_time=datetime.now()
                )

        # Обновляем статус рассылки
        mailing.status = "finished"
        mailing.save()

        return redirect('sendler:campaign_list')


def home_view(request):
    # Количество всех рассылок
    total_campaigns = Mailing.objects.count()

    # Количество активных рассылок (статус 'started')
    active_campaigns = Mailing.objects.filter(status='started').count()

    # Количество уникальных получателей
    unique_recipients = Recipient.objects.distinct().count()

    # Передаем данные в шаблон
    context = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'unique_recipients': unique_recipients,
    }

    return render(request, 'home.html', context)