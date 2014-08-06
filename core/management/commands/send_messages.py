from django.core.management.base import BaseCommand
from django.utils.translation import ugettext_lazy
from core.models import Messages
from django.utils import timezone

class Command(BaseCommand):
    args = ''
    help = ugettext_lazy("Sends out all the due text messages")

    def handle(self, *args, **options):
        for m in Messages.objects.filter(sent_when__isnull=True, when_to_send__lt=timezone.now()):
            m.send()
