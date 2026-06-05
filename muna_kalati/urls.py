"""
URL Configuration for Muna Kalati Application

This module defines all URL routes for the muna_kalati application,
including paths to views, sitemaps, static files, and media handling.

URL Patterns are organized by feature:
- General Pages: Homepage, About, Features, Privacy, Terms
- Blog/Updates: Listing and detail views with search
- Featured News: Detail view
- Jobs: Listing and detail views with search
- Press Releases: Detail view
- Social Media: Listing view with pagination
- Sitemaps: XML sitemap for SEO
- Static Files: Media and favicon handling

Features:
- Sitemap generation for SEO
- Comprehensive URL naming for reverse lookups
- Static file and media file serving
- Favicon redirect
"""

from . import views
from .views import LatestUpdateListView

from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    LatestUpdateSitemap,
    PressReleaseSitemap,
    OpenPositionSitemap,
    StaticViewSitemap
)


# Sitemap configuration for search engine crawling
# Maps sitemap names to their corresponding Sitemap classes
sitemaps = {
    'latest_updates': LatestUpdateSitemap,      # Blog posts sitemap
    'press_releases': PressReleaseSitemap,      # Press releases sitemap
    'open_positions': OpenPositionSitemap,      # Job listings sitemap
    'static': StaticViewSitemap,                # Static pages sitemap
}


urlpatterns = [
    # ==================== GENERAL PAGES ====================
    
    path(
        '',
        views.index,
        name='index'
    ),
    """
    Homepage route.
    
    View: index
    Name: 'index'
    Template: index.html
    
    Displays:
    - Hero section
    - Main landing page content
    - Featured announcements
    
    URL: /
    """

    path(
        'media_and_news/',
        views.media_and_news,
        name='media_and_news'
    ),
    """
    Media and News hub route.
    
    View: media_and_news
    Name: 'media_and_news'
    Template: media_and_news.html
    
    Displays:
    - Latest blog posts
    - Featured news
    - External media content
    - Press releases
    - Social media posts
    
    URL: /media_and_news/
    """

    path(
        'about_us/',
        views.about_us,
        name='about_us'
    ),
    """
    About Us page route.
    
    View: about_us
    Name: 'about_us'
    Template: about_us.html
    
    Displays:
    - Team member profiles
    - Testimonials and reviews
    - Organization mission
    
    URL: /about_us/
    """

    path(
        'features/',
        views.features,
        name='features'
    ),
    """
    Features page route.
    
    View: features
    Name: 'features'
    Template: features.html
    
    Displays:
    - Product/platform features
    - Service offerings
    
    URL: /features/
    """

    # ==================== BLOG/LATEST UPDATES ====================

    path(
        'updates/',
        LatestUpdateListView.as_view(),
        name='latest_updates'
    ),
    """
    Blog posts listing route (paginated).
    
    View: LatestUpdateListView (Class-based ListView)
    Name: 'latest_updates'
    Template: latest_update_list.html
    Model: LatestUpdate
    Pagination: 2 posts per page
    
    Features:
    - Pagination support
    - Ordered by creation date (newest first)
    - Browsable archive of all posts
    
    URL Patterns:
    - /updates/ (page 1)
    - /updates/?page=2 (page 2)
    - /updates/?page=N (page N)
    """

    path(
        'updates/<int:pk>/',
        views.latest_update_detail,
        name='latest_update_detail'
    ),
    """
    Individual blog post detail route.
    
    View: latest_update_detail
    Name: 'latest_update_detail'
    Template: latest_update_detail.html
    
    URL Parameters:
        pk (int): Primary key of LatestUpdate object
    
    Features:
    - Full post content display
    - Intelligent content recommendations (TF-IDF based)
    - Related articles suggestion
    
    URL Patterns:
    - /updates/1/
    - /updates/42/
    - /updates/<post_id>/
    """

    # ==================== FEATURED NEWS ====================

    path(
        'featured-news/<int:pk>/',
        views.featured_news_detail,
        name='featured_news_detail'
    ),
    """
    Featured news article detail route.
    
    View: featured_news_detail
    Name: 'featured_news_detail'
    Template: featured_news_detail.html
    
    URL Parameters:
        pk (int): Primary key of FeaturedNews object
    
    Features:
    - Featured article display
    - Content-based recommendations (word overlap)
    - Related articles suggestion
    
    URL Patterns:
    - /featured-news/1/
    - /featured-news/5/
    """

    path(
        'press-release_detail/<int:pk>/',
        views.press_release_detail,
        name='press_release_detail'
    ),
    """
    Press release detail route.
    
    View: press_release_detail
    Name: 'press_release_detail'
    Template: press_release_detail.html
    
    URL Parameters:
        pk (int): Primary key of PressRelease object
    
    Displays:
    - Official press release content
    - Publication date
    - Full text
    
    URL Patterns:
    - /press-release_detail/1/
    - /press-release_detail/3/
    """

    # ==================== JOB LISTINGS ====================

    path(
        'open-positions/',
        views.open_position_list,
        name='job_list'
    ),
    """
    Job listings page route.
    
    View: open_position_list
    Name: 'job_list'
    Template: vacancies.html
    
    Features:
    - All open positions listed
    - Newest positions first
    - Career/jobs page
    
    URL: /open-positions/
    """

    path(
        'open-positions/<int:pk>/',
        views.open_position_detail,
        name='job_details'
    ),
    """
    Individual job position detail route.
    
    View: open_position_detail
    Name: 'job_details'
    Template: open_position_detail.html
    
    URL Parameters:
        pk (int): Primary key of OpenPosition object
    
    Features:
    - Full job description
    - Requirements and responsibilities
    - Location and job type
    - Application information
    
    URL Patterns:
    - /open-positions/1/
    - /open-positions/10/
    """

    # ==================== SEARCH FUNCTIONALITY ====================

    path(
        'updates_search/',
        views.updates_search,
        name='updates_search'
    ),
    """
    Blog posts search route.
    
    View: updates_search
    Name: 'updates_search'
    Template: search_results.html
    
    GET Parameters:
        q (str): Search query (searches title, content, summary, bullet points)
        category (int): Optional category ID for filtering
    
    Features:
    - Full-text search across post fields
    - Category filtering
    - Case-insensitive matching
    
    Example URLs:
    - /updates_search/?q=education
    - /updates_search/?q=africa&category=2
    - /updates_search/?category=1
    """

    path(
        'jobs_search/',
        views.jobs_search,
        name='jobs_search'
    ),
    """
    Job listings search route.
    
    View: jobs_search
    Name: 'jobs_search'
    Template: search_results.html
    
    GET Parameters:
        q (str): Search query (searches title, description, details, type, location)
    
    Features:
    - Job search across multiple fields
    - Case-insensitive matching
    - Newest positions first
    
    Example URLs:
    - /jobs_search/?q=engineer
    - /jobs_search/?q=remote
    - /jobs_search/?q=full-time
    """

    # ==================== LEGAL PAGES ====================

    path(
        'privacy_policy/',
        views.privacy_policy,
        name='privacy_policy'
    ),
    """
    Privacy Policy page route.
    
    View: privacy_policy
    Name: 'privacy_policy'
    Template: privacy_policy.html
    
    Static page displaying privacy policy.
    
    URL: /privacy_policy/
    """

    path(
        'terms_of_use/',
        views.terms_of_use,
        name='terms_of_use'
    ),
    """
    Terms of Use page route.
    
    View: terms_of_use
    Name: 'terms_of_use'
    Template: terms_of_use.html
    
    Static page displaying terms and conditions.
    
    URL: /terms_of_use/
    """

    # ==================== CONTACT FORM ====================

    path(
        'contact/',
        views.contact_view,
        name='contact'
    ),
    """
    Contact form handler route.
    
    View: contact_view
    Name: 'contact'
    Template: Redirects to referrer
    
    HTTP Methods:
    - POST: Process contact form submission
    - GET: Redirect to referrer
    
    Form Fields:
    - name: Visitor's full name
    - email: Visitor's email address
    - message: Inquiry message
    
    Features:
    - Form validation
    - Data persistence
    - Success message display
    - Redirect to previous page
    
    URL: /contact/
    """

    # ==================== SITEMAPS (SEO) ====================

    path(
        'sitemap.xml',
        sitemap,
        {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'
    ),
    """
    XML Sitemap route for search engine crawlers.
    
    View: Django sitemap view
    Name: 'django.contrib.sitemaps.views.sitemap'
    Content-Type: application/xml
    
    Sitemaps Included:
    - latest_updates: Blog posts
    - press_releases: Press releases
    - open_positions: Job listings
    - static: Static pages
    
    Features:
    - SEO optimization
    - Search engine discovery
    - Change frequency indicators
    - Priority scores
    
    URL Patterns:
    - /sitemap.xml (index)
    - /sitemap.xml?section=latest_updates (specific sitemap)
    
    Access:
    - robots.txt directs to /sitemap.xml
    - Submit to search consoles
    """

    # ==================== STATIC FILES & FAVICON ====================

    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url('/images/favicon.ico'))
    ),
    """
    Favicon redirect route.
    
    View: RedirectView (Django generic view)
    
    Purpose:
    - Handle favicon requests
    - Redirect to static files location
    - Prevent 404 errors for browser requests
    
    Static Path:
    - /static/images/favicon.ico
    
    URL: /favicon.ico
    
    Benefits:
    - Browser compatibility
    - Cleaner logs (no favicon 404s)
    - Configurable favicon location
    """

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
STATIC AND MEDIA FILE SERVING

The + static(...) addition at the end of urlpatterns allows Django
to serve user-uploaded media files during development.

Configuration:
- MEDIA_URL: URL path for media files (from settings.py)
- MEDIA_ROOT: File system path for media files (from settings.py)

Typical Configuration in settings.py:
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Served File Types:
- Article images: /media/article_images/
- Team photos: /media/images/team/
- Hero images: /media/hero_images/
- Profile pictures: /media/profile_pictures/
- Source icons: /media/source_icons/

Production Note:
In production, use a web server (Nginx, Apache) or CDN to serve
media files instead of Django. Remove the + static(...) part.

Example Media URLs:
- /media/article_images/blog-post-1.jpg
- /media/images/team/team-member.jpg
- /media/hero_images/banner.mp4
"""


# URL NAMING CONVENTIONS
"""
URL names are used in:
1. Templates: {% url 'latest_update_detail' pk=post.id %}
2. Views: reverse('latest_update_detail', kwargs={'pk': 1})
3. Redirects: redirect('index')

Name Organization:
- Page names: 'index', 'about_us', 'features'
- List views: 'latest_updates', 'job_list'
- Detail views: 'latest_update_detail', 'job_details'
- Search: 'updates_search', 'jobs_search'
- Legal: 'privacy_policy', 'terms_of_use'
- Contact: 'contact'
- SEO: 'django.contrib.sitemaps.views.sitemap'
"""
