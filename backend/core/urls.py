from django.contrib import admin
from django.urls import path
from analytics.views import CustomTokenObtainPairView, DataIngestionView, DashboardMetricsView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/ingest/events/', DataIngestionView.as_view(), name='ingest_events'),
    path('api/dashboard/metrics/', DashboardMetricsView.as_view(), name='dashboard_metrics'),
]