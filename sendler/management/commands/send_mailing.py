from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
from sendler.models import Mailing, MailingAttempt
from datetime import datetime


class Command(BaseCommand):
    help = 'Send a mailing to all recipients'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID of the mailing to send')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']

        # Получаем рассылку по ID
        mailing = Mailing.objects.get(id=mailing_id)

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

        self.stdout.write(self.style.SUCCESS(f'Successfully sent mailing {mailing.id}'))
