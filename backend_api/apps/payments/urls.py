from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import *

app_name = 'payments'

router = DefaultRouter()
router.register(r'stk_confirmation', STKConfirmation, basename='STKConfirmation')
router.register(r'c2b_simulate', MpesaSimulateC2B, basename='MpesaSimulateC2B')
router.register(r'c2b_validation', MpesaC2BValidation, basename='MpesaC2BValidation')
router.register(r'c2b_confirmation', MpesaC2BConfirmation, basename='MpesaC2BConfirmation')
router.register(r'dpo_confirmation', DPOConfirmationView, basename='DPOConfirmationView')
router.register(r'cellulant_confirmation', CellulantWebhookView, basename='CellulantWebhookView')
router.register(r'cellulant_success', CellulantSuccessView, basename='CellulantSuccessView')
router.register(r'cellulant_pending', CellulantPendingView, basename='CellulantPendingView')
router.register(r'cellulant_fail', CellulantFailView, basename='CellulantFailView')

urlpatterns = router.urls
