from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import Http404
from django.utils.timezone import now
from django.utils.translation import gettext as _

from .models import Talk, Collection, MetaCollection


def index(request):
    return render(
        request, "core/index.html", context={
            # "up_next": Talk.objects.filter(timestamp__gte=now()).order_by('timestamp')[:10],
            "up_next": Talk.objects.order_by('timestamp')[:10],
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


def collection(request, pk):
    collection = Collection.objects.filter(collection_id=pk)
    if not collection.exists():
        collection = MetaCollection.objects.filter(collection_id=pk)
    if not collection.exists():
        raise Http404()
    else:
        collection = collection[0]
    if collection.is_meta:
        return render(
            request, "core/collection.html", context={
                "now": now(),
                "collection": collection,
            }
        )
    else:
        return render(
            request, "core/collection.html", context={
                "now": now(),
                "collection": collection,
                "talks": collection.talks.order_by('timestamp')
            }
        )