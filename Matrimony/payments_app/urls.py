from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('pay_link/<int:user_id>/', views.pay_link, name='pay_link'),
    path('api/create_order/', views.create_order, name='create_order'),
    path('api/create_external_order/<int:user_id>/', views.create_external_order, name='create_external_order'),
    path('api/verify_payment/', views.verify_payment, name='verify_payment'),
    path('api/verify_payment_link/<int:user_id>/', views.verify_payment_link, name='verify_payment_link'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('billing/', views.billing, name='billing'),
]
