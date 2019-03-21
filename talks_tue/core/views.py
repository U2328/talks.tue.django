from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.utils.translation import gettext as _

from .models import Talk


def index(request):
    return render(
        request, "core/index.html", context={
            "up_next": Talk.objects.filter(timestamp__gte=now()).order_by('timestamp')[:10],
            "hover_messages": True
        }
    )


def talk(request, pk):
    talk = get_object_or_404(Talk, pk=pk)
    if talk.timestamp < now():
        messages.warning(request, _("The Talk is already started/over!"))
    return render(
        request, "core/talk.html", context={
            "talk": talk,
            "overdue": talk.timestamp < now(),
        }
    )