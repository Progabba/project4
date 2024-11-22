from django.core.mail import send_mail
from django.utils.timezone import now

from sendler.models import MailingAttempt


def process_mailing(mailing):
    """
    Обработка рассылки: отправка писем всем получателям из mailing.
    """
    for recipient in mailing.recipients.all():
        try:
            # Отправка письма
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email="your_email@example.com",
                recipient_list=[recipient.email],
            )

            # Успешная попытка
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status="success",
                server_response="Письмо отправлено успешно."
            )
        except Exception as e:
            # Неуспешная попытка
            MailingAttempt.objects.create(
                mailing=mailing,
                recipient=recipient,
                status="failure",
                server_response=str(e)
            )

    # Обновление статуса рассылки
    mailing.status = "finished"
    mailing.end_time = now()
    mailing.save()
