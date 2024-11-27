from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from user.models import User
from .models import Recipient, Message, Mailing, MailingAttempt
from .forms import RecipientForm, MessageForm, CampaignForm
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime

from django.shortcuts import render
from django.db.models import Count, Q

from django.utils.decorators import method_decorator



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
@method_decorator(cache_page(60 * 15), name='dispatch')  # Кеширование на 15 минут
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

def mailing_statistics(request):
    # Проверка, состоит ли пользователь в группе "Менеджер"
    is_manager = request.user.groups.filter(name="менеджер").exists()

    if is_manager:
        # Для менеджера: статистика по каждому пользователю
        user_stats = (
            MailingAttempt.objects.values("mailing__user__email")  # Используем email вместо username
            .annotate(
                total_attempts=Count("id"),
                successful_attempts=Count("id", filter=Q(status="success")),
                failed_attempts=Count("id", filter=Q(status="failure")),
            )
        )
        stats = None  # Менеджеру общая статистика не нужна
    else:
        # Для обычного пользователя: только его статистика
        stats = MailingAttempt.objects.filter(mailing__user=request.user).aggregate(
            total_attempts=Count("id"),
            successful_attempts=Count("id", filter=Q(status="success")),
            failed_attempts=Count("id", filter=Q(status="failure")),
        )
        user_stats = None  # Для обычного пользователя детализация по всем пользователям не нужна

    context = {
        "stats": stats,
        "user_stats": user_stats,
        "is_manager": is_manager,
    }
    return render(request, "mailing_statistics.html", context)


# Проверка, состоит ли пользователь в группе "Менеджер"
def is_manager(user):
    return user.groups.filter(name='менеджер').exists()


# Представление для блокировки/разблокировки пользователя
@user_passes_test(is_manager)
def block_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Меняем статус пользователя
    user.is_active = not user.is_active  # Если активен, заблокируем; если заблокирован, активируем
    user.save()

    # Добавляем сообщение об успешной блокировке/разблокировке
    action = "разблокирован" if user.is_active else "заблокирован"
    messages.success(request, f"Пользователь {user.email} был {action}.")

    return redirect('user:users_list')  # Перенаправление на страницу (например, список пользователей)


# Представление для отключения/включения рассылки
@user_passes_test(is_manager)
def toggle_mailing(request, mailing_id):
    mailing = get_object_or_404(Mailing, pk=mailing_id)

    # Меняем активность рассылки
    mailing.is_active = not mailing.is_active  # Если активна, деактивируем; если неактивна, активируем
    mailing.save()

    # Добавляем сообщение об успешной деактивации/активации рассылки
    action = "деактивирована" if not mailing.is_active else "активирована"
    messages.success(request, f"Рассылка '{mailing.title}' была {action}.")

    return redirect('user:mailing_list')  # Перенаправление на страницу (например, список рассылок)