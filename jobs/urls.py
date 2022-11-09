from django.urls import path

from .views import CompanyView, CorporateView, SingleCompanyView, SingleCorporateView, GlobalConfigurationsView, AllGlobalConfigurationByCompany, SingleGlobalConfiguration, JobDetailsView, SingleJobDeatilsView

urlpatterns = [
    path('company', CompanyView.as_view()),
    path('company/<int:id>', SingleCompanyView.as_view()),
    path('corporate', CorporateView.as_view()),
    path('corporate/<int:id>', SingleCorporateView.as_view()),
    path('settings', GlobalConfigurationsView.as_view()),
    path('settings-by-company/<str:company_name>', AllGlobalConfigurationByCompany.as_view()),
    path('settings/<int:id>', SingleGlobalConfiguration.as_view()),
    path('job', JobDetailsView.as_view()),
    path('job/<int:id>', SingleJobDeatilsView.as_view())
]