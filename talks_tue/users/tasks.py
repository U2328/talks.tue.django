from celery import shared_task

from .models import User


@shared_task
def weekly_mails_task():
    ...


@shared_task
def daily_mails_task():
    ...


@shared_task
def get_next_talks(user_pk):
    user = User.objects.get(pk=pk)
    return list(set(
        talk
        for subscription in user.subscriptions.all()
        for talk in subscription.collection.related_talks
    ))
