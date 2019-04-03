from django.urls import path, reverse_lazy, re_path
from django.contrib.auth import views as auth_views
from . import views


app_name = "users"

urlpatterns = [
    path(
        "login/", auth_views.login, {
            "template_name": "users/login.html"
        }, name='login'
    ),
    path(
        "logout/", auth_views.logout, {
            "next_page": "core:index",
        }, name='logout'
    ),
    path(
        "password_reset/", auth_views.password_reset, {
            "template_name": "users/password_reset.html",
            "post_reset_redirect": reverse_lazy('users:password_reset_done')
        }, name='password_reset'
    ),
    path(
        "password_reset/done/", auth_views.password_reset_done, {
            "template_name": "users/password_reset_done.html"
        }, name='password_reset_done'
    ),
    re_path(
        "^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$", auth_views.password_reset_confirm, {
            "template_name": "users/password_change.html",
        }, name='password_reset_confirm'
    ),
    path(
        "reset/done/", auth_views.password_reset_complete, {
            "template_name": "users/password_change_done.html"
        }, name='password_reset_complete'
    ),
    path(
        "password_change/", auth_views.password_change, {
            "template_name": "users/password_change.html",
            "post_change_redirect": reverse_lazy('users:password_change_done')
        }, name='password_change'
    ),
    path(
        "password_change/done/", auth_views.password_change_done, {
            "template_name": "users/password_change_done.html"
        }, name='password_change_done'
    ),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('update/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('subscription/<int:pk>', views.SubscriptionUpdateView.as_view(), name='subscription'),
    path('subscription/<int:pk>/delete', views.subscription_delete, name='subscription_delete'),
]
