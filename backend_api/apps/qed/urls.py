from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.qed import views

app_name = "qed"
router = DefaultRouter()

router.register('dashboard', views.QedDashboardStatsView, basename='QedDashboardStatsView')
router.register('category/type', views.CategoryTypeView, basename='CategoryTypeView')
router.register('category/groups', views.CategoryGroupView, basename='CategoryGroupView')
router.register('criteria/country/(?P<category_type_id>\d+)', views.CriteriaCountryView, basename='CriteriaCountryView')
router.register('criteria/locations', views.CriteriaLocationView, basename='CriteriaLocationView')
router.register('category_type/criteria', views.CategoryTypeCriteriaView, basename='CategoryTypeCriteriaView')
router.register(r'role/privileges/(?P<role_id>\d+)', views.QedRolePrivilegeView, basename="QedRolePrivilegeView")
router.register('roles', views.QedRoleView, basename="QedRoleView")
router.register('users', views.QedView, basename="QedView")
router.register('jobs', views.JobsView, basename='JobsView')

urlpatterns = [
    path("", include(router.urls)),
]
