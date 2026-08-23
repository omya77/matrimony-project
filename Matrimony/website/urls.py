from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.Home, name='Home'),
    path('contact/', views.contact, name='contact'),
    path('stories/', views.story_page, name='story_page'),
    path('submit-story/', views.submit_story, name='submit_story'),
    path('latest-article/', views.Latest_article, name='Latest_article'),
    path('relationship-tips/', views.relationship_tips, name='relationship_tips'),
    path('marriage-advice/', views.marriage_advice, name='marriage_advice'),
    path('trust/', views.trust, name='trust'),
    path('read-more/', views.Read_more, name='Read_more'),
    path('tips/', views.tips1, name='tips1'),

    path('api/submit-counseling-query/', views.submit_counseling_query, name='submit_counseling_query'),
]
