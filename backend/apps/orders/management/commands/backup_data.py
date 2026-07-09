from django.core.management.base import BaseCommand

from apps.orders.backup import send_backup_email


class Command(BaseCommand):
    help = 'Надсилає бекап Customer/Order/OrderItem на email через Resend'

    def handle(self, *args, **options):
        sent = send_backup_email()
        if sent:
            self.stdout.write(self.style.SUCCESS('Бекап відправлено'))
        else:
            self.stdout.write(self.style.WARNING('Бекап не відправлено (нема RESEND_API_KEY/NOTIFY_EMAIL)'))
