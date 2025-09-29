from django.urls import path
from .views import (

    WebhookCreateView, 
    WebhookDetailView, 
    EventSendView
)

urlpatterns = [

    path('webhooks/', WebhookCreateView.as_view(), name='webhook-create'),
    
    path('webhooks/<int:id>/detail/', WebhookDetailView.as_view(), name='webhook-detail'),
    path('events/', EventSendView.as_view(), name='event-send'),
]
