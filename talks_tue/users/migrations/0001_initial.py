# Generated by Django 2.0.13 on 2019-03-25 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='Username')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Admin?')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email address')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified?')),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
