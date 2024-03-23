import notifications.urls
from django.contrib import admin
from django.conf import settings
from django.template.defaulttags import url
from django.urls import path, re_path, include
from django.conf.urls.static import static

from rest_framework import permissions, routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tendersure API",
        default_version="v2",
        description="Tendersure Backend",
        terms_of_service="https://www.e.tendersure.co.ke/policies/terms/",
        contact=openapi.Contact(email="devops@qedsolutions.co.ke"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    re_path(
        r"^redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    re_path(
        r"^docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "api/v1/authentication/",
        include("apps.authentication.urls", namespace="authentication"),
    ),
    path("api/v1/prequal/", include("apps.prequal.urls")),
    path("api/v1/rfq/", include("apps.rfq.urls")),
    path("api/v1/tender/", include("apps.tender.urls")),
    path("api/v1/buyer/", include("apps.buyer.urls")),
    path("api/v1/qed/", include("apps.qed.urls")),
    path("api/v1/supplier/", include("apps.suppliers.urls", namespace="suppliers")),
    path('api/v1/risk_management/', include('apps.risk_management.urls')),
    path('api/v1/auction/', include('apps.auction.urls')),
    path("api/v1/common/", include("apps.common.urls")),
    path("api/v1/projectmanagement/", include("apps.projectmanagement.urls")),
    # path("api/v1/qed/", include("apps.qed.urls")),
    # path("api/v1/contract/", include("apps.contract.urls")),
    path("api/v1/payments/", include("apps.payments.urls")),
    re_path(r'^celery-progress/', include('celery_progress.urls')),
    # path("api/v1/core/", include('apps.core.urls', namespace='notifications')),
    path("api/v1/celery_beat/", include('apps.celery_beat.urls', namespace='celery_beat'))

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
