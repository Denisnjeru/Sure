from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.tender import views

app_name = "Tender"
router = DefaultRouter()

router.register(r'categories/(?P<job_id>\d+)', views.CategoryView, basename='CategoryView')
router.register(r'sections/(?P<category_id>\d+)', views.SectionView, basename='SectionView')
router.register(r'questions/(?P<section_id>\d+)', views.QuestionView, basename='QuestionView')
router.register(r'marking/scheme/(?P<question_id>\d+)', views.MarkingSchemeView, basename='MarkingSchemeView')
router.register(r'supplier/response/(?P<question_id>\d+)/(?P<supplier_id>\d+)', views.SupplierResponseView,
                basename='SupplierResponseView')
router.register(r'qa/(?P<category_id>\d+)', views.QAView, basename='QAView')
router.register(r'qa/questions/(?P<qa_id>\d+)', views.QAQView, basename='QAQView')
router.register(r'qa/question/responses/(?P<qa_id>\d+)', views.QARView, basename='QARView')

router.register(r'dd/(?P<category_id>\d+)', views.DDView, basename='DDView')

router.register(r'items/(?P<category_id>\d+)', views.ItemView, basename='ItemView')
router.register(r'archive', views.ArchiveView, basename='ArchiveView')

router.register(r'criteria/countries', views.CriteriaCountryView, basename='CriteriaCountryView')
router.register(r'category/reports/(?P<category_id>\d+)', views.CategoryReport, basename='CategoryReport')
router.register(r'notifications/(?P<job_id>\d+)', views.JobNotificationViewSet, basename='JobNotificationViewSet')

# LETTERS
router.register(r'client/documents', views.ClientDocumentView, basename='ClientDocumentView')
router.register(r'custom/letters/(?P<category_id>\d+)', views.CustomLetterView, basename='CustomLetterView')
router.register(r'dd/letters/(?P<category_id>\d+)', views.DDLetterView, basename='DDLetterView')
router.register(r'award/letters/(?P<category_id>\d+)', views.AwardLetterView, basename='AwardLetterView')
router.register(r'regret/letters/(?P<category_id>\d+)', views.RegretLetterView, basename='RegretLetterView')

router.register(r'category/response_totals/(?P<category_id>\d+)/(?P<supplier_id>\d+)',views.SupplierFinancialTotalView,basename="SupplierFinancialTotalView")
router.register(
    r"supplier/submit/advanced_tender/(?P<supplier_id>\d+)/(?P<category_id>\d+)",
    views.SupplierAdvancedTenderView,
    basename="SupplierAdvancedTenderView"
)
router.register(r'', views.JobView, basename='JobView')

urlpatterns = [
    path('', include(router.urls)),
]
