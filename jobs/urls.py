from django.urls import path

from .views import CompanyView, CorporateView, SingleCompanyView, SingleCorporateView

urlpatterns = [
    path('company', CompanyView.as_view()),
    path('company/<int:id>', SingleCompanyView.as_view()),
    path('corporate', CorporateView.as_view()),
    path('corporate/<int:id>', SingleCorporateView.as_view())
]