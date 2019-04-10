# Generated by Django 2.0.13 on 2019-04-10 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='reminder_type',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Daily and Weekly'), (1, 'Daily'), (2, 'Weekly')], default=0, verbose_name='Reminder type'),
        ),
    ]
