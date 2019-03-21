from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('talk/<int:pk>', views.talk, name="talk")
]
