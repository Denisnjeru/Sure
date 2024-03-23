from django.urls import include, path
from rest_framework.routers import DefaultRouter
from apps.rfq import views


app_name = "Rfq"
router = DefaultRouter()
router.register(r"", views.JobView, basename="RfqView")
router.register('archive', views.ArchiveView, basename="ArchiveView")
router.register(
    r"categories/(?P<job_id>\d+)", views.RfqCategoryView, basename="RfqCategoryView"
)
router.register(r"items/(?P<category_id>\d+)", views.ItemView, basename="ItemView")
router.register(
    r"items/responses/(?P<item_id>\d+)/(?P<supplier_id>\d+)",
    views.SupplierItemResponseView,
    basename="SupplierItemResponseView",
)
router.register(
    r"category/response_totals/(?P<category_id>\d+)/(?P<supplier_id>\d+)",
    views.SupplierRfqTotalView,
    basename="SupplierRfqTotalView",
)
router.register(
    r"supplier/category_response/(?P<supplier_id>\d+)/(?P<category_id>\d+)",
    views.SupplierCategoryResponseView,
    basename="SupplierCategoryResponseView",
)
router.register(
    r"supplier/submit/advanced_rfq/(?P<supplier_id>\d+)/(?P<category_id>\d+)",
    views.SupplierAdvancedRFQView,
    basename="SupplierAdvancedRFQView"
)

urlpatterns = [path("", include(router.urls))]
