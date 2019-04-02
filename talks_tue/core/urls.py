from django.urls import path, include
from . import views

app_name = "core"

urlpatterns = [
    path('', views.index, name="index"),
    path('talk/<int:pk>', views.talk, name="talk"),
    path('collection/<int:pk>', views.collection, name="collection"),
    path('collection/<int:pk>/subscribe', views.subscribe, name="subscribe"),
]
