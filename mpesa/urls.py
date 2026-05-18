from django.urls import path
from . import views

urlpatterns = [
    path('stk-push/', views.initiate_stk_push_view, name='stk_push'),
    path('callback/', views.megapay_callback, name='megapay_callback'),
    path('status/<str:transaction_request_id>/', views.transaction_status, name='transaction_status'),
]
