from django.urls import path, include
from rest_framework.routers import DefaultRouter

from  . import views

app_name = "risk_management"
router = DefaultRouter()

router.register(r'', views.JobView, basename='RiskJobView')
router.register(r'categories/(?P<job_id>\d+)', views.CategoryView, basename='RiskCategoryView')
router.register(r'sections/(?P<category_id>\d+)', views.SectionView, basename='RiskSectionView')
router.register(r'questions/(?P<section_id>\d+)', views.QuestionView, basename='RiskQuestionView')
router.register(r'marking/scheme/(?P<question_id>\d+)', views.MarkingSchemeView, basename='RiskMarkingSchemeView')
router.register(r'supplier/response/(?P<question_id>\d+)/(?P<supplier_id>\d+)', views.SupplierResponseView,
                basename='RiskSupplierResponseView')
router.register(r'qa/(?P<category_id>\d+)', views.QAView, basename='RiskQAView')
router.register(r'qa/questions/(?P<qa_id>\d+)', views.QAQView, basename='RiskQAQView')
router.register(r'qa/question/responses/(?P<qa_question_id>\d+)', views.QARView, basename='RiskQARView')
router.register(r'supportingdocuments/(?P<job_id>\d+)', views.RiskSupportingDocumentView, basename='RiskSupportingDocumentView')
router.register(r'categorysupportingdocuments/(?P<category_id>\d+)', views.RiskCategorySupportingDocumentView, basename='RiskCategorySupportingDocumentView')
urlpatterns = [
    path('', include(router.urls)),
]