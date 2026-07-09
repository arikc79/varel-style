from django.urls import path
from .views import BackupTriggerView, OrderCreateView, OrderListView

urlpatterns = [
    path('', OrderCreateView.as_view()),
    path('list/', OrderListView.as_view()),
    path('backup/', BackupTriggerView.as_view()),
]
