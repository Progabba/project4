from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from sendler.models import Mailing, Recipient

class Command(BaseCommand):
    help = "Отправка сообщений по рассылке"

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status="created")
        for mailing in mailings:
            recipients = mailing.recipients.all()
            for recipient in recipients:
                try:
                    send_mail(
                        subject=mailing.message.subject,
                        message=mailing.message.body,
                        from_email="your_email@example.com",
                        recipient_list=[recipient.email],
                    )
                    self.stdout.write(self.style.SUCCESS(f"Письмо отправлено {recipient.email}"))
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Ошибка при отправке: {e}"))
            mailing.status = "started"
            mailing.save()
