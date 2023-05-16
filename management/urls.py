from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views,import_excel,sample_form_has_parameter,formula_algorithm

router = DefaultRouter()
router.register('client-category', views.ClientCategoryViewSet, basename="apis/client_category")
router.register('sample-form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('test-result', views.TestResultViewSet, basename="test_result")
router.register('commodity-category', views.CommodityCategoryViewSet, basename="commodity_category")
router.register('sample-form-has-parameter-assign-users', sample_form_has_parameter.SampleFormHasParameterViewSet, basename="SampleFormHasParameterViewSet")
router.register('sample-form-has-payment', views.PaymentViewSet, basename="PaymentViewSet")
router.register('sample-form-has-calculate-resuslt',formula_algorithm.SampleFormParameterFormulaCalculateViewSet,basename="SampleFormParameterFormulaCalculateViewSet")


urlpatterns = [
    path('', include(router.urls)),
    path('formula-api/', formula_algorithm.FormulaApiCalculate.as_view(), name='custom_endpoint'),
    path('import-excel-bulk/',import_excel.ImportExcel,name="ImportExcel")
]