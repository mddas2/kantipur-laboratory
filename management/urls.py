from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views,import_excel,sample_form_has_parameter,formula_algorithm,raw_data
from . import verfier

router = DefaultRouter()
router.register('client-category', views.ClientCategoryViewSet, basename="apis/client_category")
router.register('sample-form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('test-result', views.TestResultViewSet, basename="test_result")
router.register('commodity-category', views.CommodityCategoryViewSet, basename="commodity_category")
router.register('sample-form-has-parameter-assign-users', sample_form_has_parameter.SampleFormHasParameterViewSet, basename="SampleFormHasParameterViewSet")
router.register('sample-form-has-payment', views.PaymentViewSet, basename="PaymentViewSet")
router.register('sample-form-has-calculate-result',formula_algorithm.SampleFormParameterFormulaCalculateViewSet,basename="SampleFormParameterFormulaCalculateViewSet")
router.register('sample-form-has-verifier',verfier.SampleFormHasVerifierViewSet,basename="SampleFormHasVerifierViewSet")


urlpatterns = [
    path('', include(router.urls)),
    path('get-formula-fields/', formula_algorithm.FormulaApiGetFields.as_view(), name='custom_endpoint'),
    path('formula-calculate/', formula_algorithm.FormulaApiCalculate.as_view(), name='custom_endpoint'),

    path('formula-result-save/', formula_algorithm.FormulaApiCalculateSave.as_view(), name='custom_endpoint'),

    path('parameter-has-result-recheck/', formula_algorithm.ParameterHasResultRecheck.as_view(), name='single_recheck'),

    path('detail-raw-data-sheet/<int:sample_form_has_parameter>/', raw_data.rawDataDetail.as_view(), name='rawData'),
    path('sample-form-raw-data-sheet/<str:sample_form>/', raw_data.rawDataForSampleForm.as_view(), name='rawDataSupervisor'),
    
    path('get-parameter-to-verified/<int:sample_form_id>/', formula_algorithm.FormulaGetToVerifier.as_view(), name='formula-calculte-verifier'),
    path('import-excel-bulk/',import_excel.ImportExcel,name="ImportExcel")
]