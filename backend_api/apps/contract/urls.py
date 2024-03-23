from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.contract import views

app_name = "Contract"
router = DefaultRouter()
router.register(r'jobs', views.JobsView, basename='JobsView')
router.register(r'category', views.CategorySupplierView, basename='CategorySupplierView')
router.register(r'contracts', views.ContractView, basename='ContractView')
router.register(r'supplier_contracts', views.SupplierContractView, basename='SupplierContractView')
router.register(r'sections', views.ContractSectionView, basename='ContractSectionView')
router.register(r'templates', views.ContractTemplateView, basename='ContractTemplateView')
router.register(r'revisions', views.SupplierContractRevisionsView, basename='SupplierContractRevisionsView')
# router.register(r'', views.ContractDocumentView, basename='ContractDocumentView')

urlpatterns = [
    path('', include(router.urls)),
]
