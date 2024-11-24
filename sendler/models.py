from django.db import models

from user.models import User


# Управление клиентами
class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="Ф.И.О.")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    user = models.ForeignKey(
        User,  # Ссылаемся на кастомную модель User
        on_delete=models.CASCADE,  # При удалении пользователя удаляем все его рассылки
        verbose_name="Пользователь",  # Человекочитаемое имя поля
        related_name="recipients",  # Связь для обратного доступа через пользователя
        null=True,  # Разрешаем пустые значения
        blank=True,  # Разрешаем оставлять поле пустым в формах
    )

    def __str__(self):
        return f"{self.full_name} ({self.email})"


# Управление сообщениями
class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма")

    user = models.ForeignKey(
        User,  # Ссылаемся на кастомную модель User
        on_delete=models.CASCADE,  # При удалении пользователя удаляем все его рассылки
        verbose_name="Пользователь",  # Человекочитаемое имя поля
        related_name="messages",  # Связь для обратного доступа через пользователя
        null=True,  # Разрешаем пустые значения
        blank=True,  # Разрешаем оставлять поле пустым в формах
    )

    def __str__(self):
        return self.subject


# Управление рассылками
class Mailing(models.Model):
    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    ]

    start_time = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_time = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = models.ForeignKey("Message", on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField("Recipient", verbose_name="Получатели")
    user = models.ForeignKey(
        User,  # Ссылаемся на кастомную модель User
        on_delete=models.CASCADE,  # При удалении пользователя удаляем все его рассылки
        verbose_name="Пользователь",  # Человекочитаемое имя поля
        related_name="mailings",  # Связь для обратного доступа через пользователя
        null=True,  # Разрешаем пустые значения
        blank=True,  # Разрешаем оставлять поле пустым в формах
    )

    def __str__(self):
        return f"Рассылка {self.pk} ({self.get_status_display()})"


# Попытка рассылок
class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ("success", "Успешно"),
        ("failure", "Не успешно"),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name="Рассылка")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервера", blank=True, null=True)

    def __str__(self):
        return f"Попытка {self.mailing.pk} - {self.get_status_display()}"