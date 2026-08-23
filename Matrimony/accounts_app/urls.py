from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.registration, name='registration'),
    path('registration/', views.registration, name='registration_alt'),
    
    # API endpoints for frontend UI integration
    path('api/send_otp/', views.api_send_otp, name='api_send_otp'),
    path('api/verify_otp/', views.api_verify_otp, name='api_verify_otp'),
    
    path('api/send_mobile_otp/', views.api_send_mobile_otp, name='api_send_mobile_otp'),
    path('api/verify_mobile_otp/', views.api_verify_mobile_otp, name='api_verify_mobile_otp'),
    
    path('api/send_id_otp/', views.api_send_id_otp, name='api_send_id_otp'),
    path('api/verify_id_otp/', views.api_verify_id_otp, name='api_verify_id_otp'),
    
    path('api/create_user/', views.api_create_user, name='api_create_user'),
    path('api/send_forgot_otp/', views.api_send_forgot_otp, name='api_send_forgot_otp'),
    path('api/verify_forgot_otp/', views.api_verify_forgot_otp, name='api_verify_forgot_otp'),
    
    path('settings/', views.settings, name='settings'),
    path('update-password/', views.update_password, name='update_password'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
