from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='chat'),
    path('requests/', views.requests, name='requests'),
    path('gestures/', views.gestures, name='gestures'),

    # APIs for Interest & Chat restriction
    path('api/navbar-counts/', views.api_navbar_counts, name='api_navbar_counts'),
    path('api/express-interest/', views.api_express_interest, name='api_express_interest'),
    path('api/check-interest/', views.api_check_interest, name='api_check_interest'),
    path('api/accept-interest/', views.api_accept_interest, name='api_accept_interest'),
    path('api/reject-interest/', views.api_reject_interest, name='api_reject_interest'),
    path('api/send-message/', views.send_message, name='send_message'),
    path('api/delete-message/<int:msg_id>/', views.api_delete_message, name='api_delete_message'),
    path('api/delete-chat/<int:user_id>/', views.api_delete_chat, name='api_delete_chat'),
    path('api/mark-notifications-read/', views.api_mark_notifications_read, name='api_mark_notifications_read'),
    path('api/report-user/', views.api_report_user, name='api_report_user'),

    path('api/fetch-messages/<int:user_id>/', views.fetch_messages, name='fetch_messages'),
    path('api/save-profile/', views.api_save_profile, name='api_save_profile'),
    path('api/log-visit/<int:user_id>/', views.api_log_visit, name='api_log_visit'),

    # Search and Matches
    path('search/basic/', views.basic_search, name='basic_search'),
    path('search/advanced/', views.advanced_search, name='advanced_search'),
    path('search/ai/', views.ai_search, name='ai_search'),
    path('search/saved/', views.saved_searches, name='saved_searches'),
    path('matches/recommended/', views.recomended_matches, name='recomended_matches'),
    path('matches/nearby/', views.nearby_match, name='nearby_match'),
    path('matches/today/', views.todays_matches, name='todays_matches'),
    path('matches/todays/', views.todays_matches),  # Alias for backward compatibility
    path('matches/matches1/', views.matches1, name='matches1'),
    path('matches/matches2/', views.matches2, name='matches2'),
    path('matches/Ai-match/', views.Ai_match, name='Ai_match'),
    path('featured/brides/', views.featured_brides, name='featured_brides'),
    path('featured/grooms/', views.featured_grooms, name='featured_grooms'),


    path('block_user/', views.block_user, name='block_user'),
    path('report_user/', views.report_user, name='report_user'),
]

