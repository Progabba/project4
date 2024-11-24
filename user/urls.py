from django.urls import path, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView

from .apps import UserConfig
from .views import UserCreateView, email_verification

app_name = UserConfig.name

urlpatterns = [

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-conform/<str:token>/', email_verification, name='email-conform'),

    path('password-reset/',
         PasswordResetView.as_view(
             template_name="user/password_reset_form.html",
             email_template_name="user/password_reset_email.html",
             success_url=reverse_lazy("user:password_reset_done")
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="user/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="user/password_reset_confirm.html",
             success_url=reverse_lazy("user:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="user/password_reset_complete.html"),
         name='password_reset_complete'),

]
