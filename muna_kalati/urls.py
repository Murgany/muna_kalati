from . import views
from .views import LatestUpdateListView

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('media_and_news/', views.media_and_news, name='media_and_news'),
    path('about_us/', views.about_us, name='about_us'),
    path('features/', views.features, name='features'),

    # LatestUpdate URLs
    path('updates/', LatestUpdateListView.as_view(), name='latest_updates'),
    path('updates/<int:pk>/', views.latest_update_detail, name='latest_update_detail'),

    # FeaturedNews URLs
    path('featured-news/<int:pk>/', views.featured_news_detail, name='featured_news_detail'),

    path('press-release_detail/<int:pk>/', views.press_release_detail, name='press_release_detail'),

    # OpenPosition URLs
    path('open-positions/', views.open_position_list, name='job_list'),
    path('open-positions/<int:pk>/', views.open_position_detail, name='job_details'),

    path('updates_search/', views.updates_search, name='updates_search'),
    path('jobs_search/', views.jobs_search, name='jobs_search'),

    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('terms_of_use/', views.terms_of_use, name='terms_of_use'),

    path('contact/', views.contact_view, name='contact'), 


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
