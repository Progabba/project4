from django.shortcuts import render

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
class RecipientListView(ListView):
    model = Recipient
    template_name = "recipients/recipient_list.html"
    context_object_name = "recipients"

# Создание клиента
class RecipientCreateView(CreateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy('sendler:recipient_list')  # Используем reverse_lazy для отложенного реверса

# Редактирование клиента
class RecipientUpdateView(UpdateView):
    model = Recipient
    form_class = RecipientForm
    template_name = "recipients/recipient_form.html"
    success_url = reverse_lazy('sendler:recipient_list')  # Используем reverse_lazy для отложенного реверса

# Удаление клиента
class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = "recipients/recipient_confirm_delete.html"
    success_url = reverse_lazy('sendler:recipient_list')  # Используем reverse_lazy для отложенного реверса

# Список сообщений
class MessageListView(ListView):
    model = Message
    template_name = "messages/message_list.html"
    context_object_name = "messages"

# Создание сообщения
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/message_form.html"
    success_url = reverse_lazy('sendler:message_list')

# Редактирование сообщения
class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "messages/message_form.html"
    success_url = reverse_lazy('sendler:message_list')

# Удаление сообщения
class MessageDeleteView(DeleteView):
    model = Message
    template_name = "messages/message_confirm_delete.html"
    success_url = reverse_lazy('sendler:message_list')

# Список рассылок
class CampaignListView(ListView):
    model = Mailing
    template_name = "campaigns/campaign_list.html"
    context_object_name = "campaigns"

# Создание рассылки
class CampaignCreateView(CreateView):
    model = Mailing
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy('sendler:campaign_list')

# Редактирование рассылки
class CampaignUpdateView(UpdateView):
    model = Mailing
    form_class = CampaignForm
    template_name = "campaigns/campaign_form.html"
    success_url = reverse_lazy('sendler:campaign_list')

# Удаление рассылки
class CampaignDeleteView(DeleteView):
    model = Mailing
    template_name = "campaigns/campaign_confirm_delete.html"
    success_url = reverse_lazy('sendler:campaign_list')

# Детали рассылки
class CampaignDetailView(DetailView):
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