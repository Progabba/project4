from django.urls import path


from django.contrib.auth.views import LoginView, LogoutView

from .apps import UserConfig
from .views import UserCreateView, email_verification

app_name = UserConfig.name

urlpatterns = [

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email-conform/<str:token>/', email_verification, name='email-conform'),

]
