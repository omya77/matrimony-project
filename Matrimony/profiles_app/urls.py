from django.urls import path
from . import views

urlpatterns = [
    path('my-profile/', views.my_profile, name='my_profile'),
    path('saved-profiles/', views.saved_profiles, name='saved_profiles'),
    path('verified-profiles/', views.verified_profiles, name='verified_profiles'),
    path('personal/', views.personal, name='personal'),
    # path('my-profile-data/', views.my_profile_data, name='my_profile_data'),
    path('who-viewed-me/', views.who_viewed_me, name='who_viewed_me'),
    path('upload-photo/', views.upload_photo, name='upload_photo'),
    path('update_privacy/', views.update_privacy, name='update_privacy'),
    path('upload_gallery/', views.upload_gallery, name='upload_gallery'),
    path('upload_kyc/', views.upload_kyc, name='upload_kyc'),
]
