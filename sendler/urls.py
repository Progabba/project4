from django.urls import path
from . import views
from .apps import SendlerConfig

app_name = SendlerConfig.name

urlpatterns = [
    path("", views.RecipientListView.as_view(), name="recipient_list"),
    path("create/", views.RecipientCreateView.as_view(), name="recipient_create"),
    path("<int:pk>/edit/", views.RecipientUpdateView.as_view(), name="recipient_edit"),
    path("<int:pk>/delete/", views.RecipientDeleteView.as_view(), name="recipient_delete"),
]
