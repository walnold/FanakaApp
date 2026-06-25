from django.urls import path
from .views import AnalyticsViewSet

urlpatterns = [
    path("", AnalyticsViewSet.as_view({"get": "list"}), name='analytics-overview')
]
