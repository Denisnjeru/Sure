from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.buyer import views

app_name = "Buyer"
router = DefaultRouter()

router.register(r'users', views.BuyerView, basename='BuyerView')
router.register(r'roles', views.BuyerRoleView, basename='BuyerRoleView')
router.register(r'privileges', views.BuyerPrivilegeView, basename='BuyerPrivilegeView')
router.register(r'role/privileges/(?P<role_id>\d+)', views.BuyerRolePrivilegeView, basename='BuyerRolePrivilegeView')
router.register(r'jobs', views.JobsView, basename='JobsView')
router.register(r'', views.CompanyView, basename='CompanyView')

urlpatterns = [
    path('', include(router.urls)),
]