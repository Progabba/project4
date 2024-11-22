from django.urls import path

from sendler.views import RecipientListView, RecipientCreateView, RecipientUpdateView, RecipientDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, CampaignListView, CampaignCreateView, \
    CampaignDetailView, CampaignUpdateView, CampaignDeleteView, SendMailingView, home_view
from .apps import SendlerConfig

app_name = SendlerConfig.name

urlpatterns = [
    path("recipients/", RecipientListView.as_view(), name="recipient_list"),
    path("recipients/create/", RecipientCreateView.as_view(), name="recipient_create"),
    path("recipients/<int:pk>/edit/", RecipientUpdateView.as_view(), name="recipient_edit"),
    path("recipients/<int:pk>/delete/", RecipientDeleteView.as_view(), name="recipient_delete"),

# URL-ы для сообщений
    path("messages/", MessageListView.as_view(), name="message_list"),
    path("messages/create/", MessageCreateView.as_view(), name="message_create"),
    path("messages/<int:pk>/edit/", MessageUpdateView.as_view(), name="message_edit"),
    path("messages/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("campaigns/<int:pk>/send/", SendMailingView.as_view(), name="send_mailing"),

    # URL-ы для рассылок
    path("campaigns/", CampaignListView.as_view(), name="campaign_list"),
    path("campaigns/create/", CampaignCreateView.as_view(), name="campaign_create"),
    path("campaigns/<int:pk>/", CampaignDetailView.as_view(), name="campaign_detail"),
    path("campaigns/<int:pk>/edit/", CampaignUpdateView.as_view(), name="campaign_edit"),
    path("campaigns/<int:pk>/delete/", CampaignDeleteView.as_view(), name="campaign_delete"),

    path('', home_view, name='home'),
]
