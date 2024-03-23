from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.suppliers import views

# app_name = "suppliers"
app_name = "suppliers"
router = DefaultRouter()
router.register(
    r"register", views.SupplierRegisterView, basename="SupplierRegisterView"
)
router.register(r"list", views.SupplierView, basename="SupplierView")
router.register(
    r"company/users",
    views.SupplierCompanyUserView,
    basename="SupplierCompanyUserView",
)
router.register(r"company", views.SupplierCompanyView, basename="SupplierCompanyView")
router.register(r"dashboard/stats", views.SupplierDashboardStatsView, basename="SupplierDashboardStatsView")
router.register(r"dashboard/companies_open_jobs", views.CompaniesWithOpenJobsView, basename="CompaniesWithOpenJobsView")
router.register(r"category_order", views.CategoryOrderView, basename="CategoryOrderView")
router.register(r"roles", views.SupplierRoleView, basename="SupplierRoleView")
router.register(r'role/privileges/(?P<role_id>\d+)', views.SupplierRolePrivilegeView, basename='SupplierRolePrivilegeView')
router.register(r"profile", views.SupplierCompanyProfileView, basename="SupplierCompanyProfileView")
router.register(r"rfqs", views.SupplierRFQView, basename="SupplierRFQView")
router.register(r"archive", views.ArchiveView, basename="ArchiveView")
router.register(r"auction/participating", views.ParticipatingAuctionView, basename="ParticipatingAuctionView")

router.register(r"prequal/ordered/categories", views.OrderedPreQualCategoryView, basename="OrderedPreQualCategoryView")
router.register(r"prequal/open/categories", views.OpenPrequalJobsView, basename="OpenPrequalJobsView")
router.register(r"tender/ordered/categories", views.OrderedTenderCategoryView, basename="OrderedTenderCategoryView")
router.register(r"tender/open/categories", views.OpenTenderJobsView, basename="OpenTenderJobsView")

urlpatterns = [
    path("", include(router.urls)),
]
