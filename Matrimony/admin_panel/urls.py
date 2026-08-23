from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Custom OTP Password Reset
    path('forgot-password/', views.admin_forgot_password, name='admin_forgot_password'),
    path('verify-otp/', views.admin_verify_otp, name='admin_verify_otp'),
    path('reset-password/', views.admin_reset_password, name='admin_reset_password'),

    # Password Reset URLs (Fallback/Standard)
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='admin_panel/password_reset_form.html',
        email_template_name='admin_panel/password_reset_email.html',
        subject_template_name='admin_panel/password_reset_subject.txt',
        success_url='/admin_panel/password_reset/done/'
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='admin_panel/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='admin_panel/password_reset_confirm.html',
        success_url='/admin_panel/reset/done/'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='admin_panel/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),

    path('', views.dashboard, name='admin_dashboard'),
    path('approvals/', views.profile_approvals, name='profile_approvals'),
    path('api/approve_user/', views.approve_user, name='approve_user'),
    path('api/reject_user/', views.reject_user, name='reject_user'),
    path('api/delete_user/', views.delete_user, name='delete_user'),
    path('api/approve_photo/', views.approve_photo, name='approve_photo'),
    path('api/reject_photo/', views.reject_photo, name='reject_photo'),
    
    # Auth Management (Omkar Module)
    path('auth/users/', views.auth_users, name='auth_users'),
    path('auth/login-logs/', views.auth_login_logs, name='auth_login_logs'),
    path('auth/security/', views.auth_security, name='auth_security'),
    path('auth/roles/', views.auth_roles, name='auth_roles'),
    path('api/update_user_role/', views.update_user_role, name='update_user_role'),

    # Gauri Modules
    path('profiles/manage/', views.gauri_manage_profiles, name='gauri_manage_profiles'),
    path('profiles/photos/', views.gauri_photo_approvals, name='gauri_photo_approvals'),
    path('profiles/preferences/', views.gauri_partner_preferences, name='gauri_partner_preferences'),
    path('profiles/view/<int:profile_id>/', views.admin_view_profile, name='admin_view_profile'),

    # Sandhya Interactions Admin
    path('interactions/search/', views.sandhya_match_search, name='sandhya_match_search'),
    path('interactions/requests/', views.sandhya_pending_requests, name='sandhya_pending_requests'),


    # Tejaswini Extensions
    path('api/toggle-user-status/', views.toggle_user_status, name='toggle_user_status'),
    path('revenue-reports/', views.revenue_reports, name='revenue_reports'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('api/toggle-story-status/', views.toggle_story_status, name='toggle_story_status'),
    path('api/toggle-setting/', views.toggle_setting, name='toggle_setting'),


    # Mukta's Payments Module
    path('memberships/', views.mukta_memberships, name='mukta_memberships'),
    path('api/save-plan/', views.save_plan, name='save_plan'),
    path('api/toggle-plan-status/', views.toggle_plan_status, name='toggle_plan_status'),
    path('api/delete-plan/', views.delete_plan, name='delete_plan'),
    path('billing-history/', views.mukta_billing, name='mukta_billing'),
    path('export-billing-csv/', views.export_billing_csv, name='export_billing_csv'),
    path('payment-gateway/', views.mukta_gateway, name='mukta_gateway'),
    path('api/save-payment-gateway/', views.save_payment_gateway, name='save_payment_gateway'),
    
    # Sarthak's Frontend & Web Module
    path('website-content/', views.sarthak_website_content, name='sarthak_website_content'),
    path('chat-logs/', views.sarthak_chat_logs, name='sarthak_chat_logs'),
    path('api/save-website-content/', views.save_website_content, name='save_website_content'),
    
    # Missing Features added based on script
    path('master-data/', views.manage_master_data, name='manage_master_data'),
    path('kyc-approvals/', views.kyc_approvals, name='kyc_approvals'),
    path('reports/', views.reported_profiles, name='reported_profiles'),
    path('counseling-queries/', views.counseling_queries, name='counseling_queries'),
    path('contact-queries/', views.contact_queries, name='contact_queries'),
    path('api/toggle-contact-status/', views.toggle_contact_status, name='toggle_contact_status'),
]
