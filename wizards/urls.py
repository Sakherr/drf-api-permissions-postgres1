from django.urls import path
from .views import WizardList, WizardDetail

urlpatterns = [
  path('', WizardList.as_view(), name='wizard_list'),
  path('<int:pk>/', WizardDetail.as_view(), name='wizard_detail'),
]
