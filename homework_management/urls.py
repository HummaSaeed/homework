"""homework_management URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # API v1 Routes
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/schools/', include('schools.urls')),
    path('api/v1/classes/', include('classes.urls')),
    path('api/v1/subjects/', include('subjects.urls')),
    path('api/v1/homework/', include('homework.urls')),
    path('api/v1/submissions/', include('submissions.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/reports/', include('reports.urls')),
    path('api/v1/files/', include('files.urls')),
    path('api/v1/audit-logs/', include('audit_logs.urls')),

    # OpenAPI / Swagger Documentation
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
