from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apply', views.apply_view, name='apply'),
    path('processing', views.processing_view, name='processing'),
    path('loan-offers', views.loan_offers_view, name='loan_offers'),
    path('payment-success', views.payment_success_view, name='payment_success'),
    path('privacy', views.privacy_view, name='privacy'),
    path('terms', views.terms_view, name='terms'),
    path('contact', views.contact_view, name='contact'),
    path('api/submit-application/', views.submit_application, name='submit_application'),
    path('api/loan-amounts/', views.get_loan_amounts_api, name='loan_amounts_api'),
]
