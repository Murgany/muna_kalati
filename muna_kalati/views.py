"""
Django Views for Muna Kalati Application

This module contains all view functions and classes for rendering pages,
handling form submissions, and serving content to users.

Views include:
- Homepage and general site pages
- Blog/Latest Updates listing and detail views
- Featured News detail view
- Job Listings and detail views
- Press Releases detail view
- Social Media Posts listing
- Search functionality
- Contact form handling
- Utility views (privacy, terms, robots.txt)

Key Features:
- Content recommendation engine using TF-IDF and cosine similarity
- Advanced search with category filtering
- SEO-friendly meta tags
- Pagination for list views
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import (
    HeroSection, LatestUpdate, FeaturedNews, OpenPosition,
    ExternalMediaContent, PressRelease, SocialMediaPost,
    Category, TeamMember, Review
)
import time
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib import messages
from .forms import ContactForm
import re
from django.http import HttpResponse


def updates_search(request):
    """
    Search view for blog posts and latest updates.
    
    Supports searching by:
    - Title (case-insensitive)
    - Bullet points
    - Content
    - Summary
    - Category filter
    
    GET Parameters:
        q (str): Search query string
        category (int): Optional category ID to filter by
    
    Returns:
        HttpResponse: Rendered search_results.html with filtered updates
    
    Context:
        latest_updates (QuerySet): Filtered LatestUpdate objects
        query (str): The search query
        categories (QuerySet): All available categories for dropdown filter
    
    Example:
        GET /updates_search/?q=education&category=1
    """
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    # Build dynamic Q filters
    filters = Q()
    
    if query:
        # Search across multiple fields
        filters |= (Q(title__icontains=query) | 
                    Q(bullet_points__icontains=query) | 
                    Q(content__icontains=query) | 
                    Q(summary__icontains=query))
    
    if category_id:
        # Apply category filter if provided
        filters &= Q(category_id=category_id)

    latest_updates = LatestUpdate.objects.filter(filters).order_by('-id')
    
    context = {
        'latest_updates': latest_updates,
        'query': query,
        'categories': Category.objects.all(),
    }
    
    return render(request, 'search_results.html', context)


def jobs_search(request):
    """
    Search view for job listings.
    
    Supports searching by:
    - Job title
    - Brief description
    - Job details
    - Job type (Full-time, Part-time, etc.)
    - Location
    
    GET Parameters:
        q (str): Search query string
    
    Returns:
        HttpResponse: Rendered search_results.html with filtered jobs
    
    Context:
        jobs (QuerySet): Filtered OpenPosition objects
        query (str): The search query
    
    Example:
        GET /jobs_search/?q=software+engineer
    """
    query = request.GET.get('q')
    
    if query:
        # Search across job-related fields
        jobs = OpenPosition.objects.filter(
            Q(job_title__icontains=query) |
            Q(brief_description__icontains=query) |
            Q(details__icontains=query) |
            Q(job_type__icontains=query) |
            Q(location__icontains=query)
        ).order_by('-posted_on')

        context = {
            'jobs': jobs,
            'query': query,
        }
    else:
        context = {}
    
    return render(request, 'search_results.html', context)


def index(request):
    """
    Homepage view.
    
    Displays the main landing page with hero section and featured content.
    
    Returns:
        HttpResponse: Rendered index.html with hero section
    
    Context:
        hero_section (HeroSection): Latest HeroSection object
        meta_title (str): Page title for SEO
        meta_description (str): Page description for SEO
    
    Note:
        Uses .last() to get the most recent hero section.
        Typically only one HeroSection should exist.
    """
    hero_section = HeroSection.objects.last() 
    context = {
        'hero_section': hero_section,
        "meta_title": "Empowering African Children Through Afrocentric Education | Muna Kalati",
        "meta_description": "Muna Kalati offers Afrocentric storybooks, audiobooks, and animated videos in 39 African languages, empowering children to be confident thinkers.",
    } 
    return render(request, 'index.html', context)


def about_us(requrst):
    """
    About Us page view.
    
    Displays team members and testimonial reviews.
    
    Parameters:
        request (HttpRequest): The HTTP request object
    
    Returns:
        HttpResponse: Rendered about_us.html with team and reviews
    
    Context:
        team_members (QuerySet): All TeamMember objects sorted by name
        ratings (QuerySet): Top 4 Review objects (highest rated first)
        meta_title (str): Page title for SEO
        meta_description (str): Page description for SEO
    
    Note:
        Parameter is named 'requrst' (typo) but works as intended.
        Consider renaming to 'request' in future refactor.
    """
    team_members = TeamMember.objects.all().order_by('name')
    ratings = Review.objects.all().order_by('-rating')[:4]
    context = {
        'team_members': team_members,
        'ratings': ratings,
        "meta_title": "Empowering African Children Through Afrocentric Education | Muna Kalati",
        "meta_description": "Muna Kalati offers Afrocentric storybooks, audiobooks, and animated videos in 39 African languages, empowering children to be confident thinkers.",
    }
    return render(requrst, 'about_us.html', context)


def features(request):
    """
    Features page view.
    
    Displays product/platform features.
    
    Returns:
        HttpResponse: Rendered features.html
    
    Context:
        img_name (str): Dynamically generated filename for QR code
                       (e.g., 'qr_1686325234.567.png')
    
    Note:
        QR code generation logic appears to be handled in template
        with this filename as reference.
    """
    img_name = f'qr_{time.time()}.png'
    return render(request, 'features.html', {'img_name': img_name})


def media_and_news(request):
    """
    Media and News hub view.
    
    Comprehensive view displaying latest blog posts, featured news,
    external media content, press releases, and social media posts.
    
    Returns:
        HttpResponse: Rendered media_and_news.html with all content
    
    Context:
        updates (QuerySet): Latest 4 LatestUpdate objects
        featured_news (FeaturedNews): Most recent FeaturedNews object
        external_media (QuerySet): Latest 2 ExternalMediaContent objects
        press_releases (QuerySet): Latest 2 PressRelease objects
        posts (QuerySet): Latest 4 SocialMediaPost objects
    
    Template Variables Explained:
        - updates: Blog articles for quick viewing
        - featured_news: Highlighted article (one-to-one)
        - external_media: Third-party mentions/coverage
        - press_releases: Official announcements
        - posts: Social media engagement
    """
    updates = LatestUpdate.objects.all().order_by('-created')[:4]
    featured_news = FeaturedNews.objects.last()
    external_media = ExternalMediaContent.objects.all().order_by('-created')[:2]
    press_releases = PressRelease.objects.all().order_by('-created')[:2]
    posts = SocialMediaPost.objects.all().order_by('-created')[:4]
    
    return render(request, 'media_and_news.html', {
        'updates': updates,
        'featured_news': featured_news,
        'external_media': external_media,
        'press_releases': press_releases,
        'posts': posts
    })


def press_release_detail(request, pk):
    """
    Press Release detail view.
    
    Displays a single press release with full content.
    
    Parameters:
        request (HttpRequest): HTTP request object
        pk (int): Primary key of the PressRelease object
    
    Returns:
        HttpResponse: Rendered press_release_detail.html
        404: If press release not found
    
    Context:
        release (PressRelease): The requested press release object
    
    URL Pattern:
        /press-release/<int:pk>/
    
    Example:
        GET /press-release/5/
    """
    release = get_object_or_404(PressRelease, pk=pk)
    return render(request, 'press_release_detail.html', {'release': release})


class LatestUpdateListView(ListView):
    """
    List view for displaying paginated blog posts.
    
    Displays all LatestUpdate objects in paginated format.
    
    Attributes:
        model (Model): LatestUpdate model
        template_name (str): 'latest_update_list.html'
        context_object_name (str): 'latest_updates' (variable name in template)
        paginate_by (int): 2 updates per page (customizable)
    
    URL Pattern:
        /updates/
    
    Template Context:
        latest_updates (list): Paginated list of LatestUpdate objects
        page_obj (Page): Django Page object for pagination
        is_paginated (bool): Whether list is paginated
        paginator (Paginator): Django Paginator object
    
    Example Query:
        GET /updates/
        GET /updates/?page=2
    
    Note:
        Pagination limit of 2 can be increased by changing paginate_by
    """
    model = LatestUpdate
    template_name = 'latest_update_list.html'
    context_object_name = 'latest_updates'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        """
        Override to add custom context if needed in future.
        
        Returns:
            dict: Context dictionary with paginated updates
        """
        context = super().get_context_data(**kwargs)
        return context


def latest_update_detail(request, pk):
    """
    Blog post detail view with intelligent recommendations.
    
    Displays a single blog post with recommended similar posts
    using TF-IDF vectorization and cosine similarity algorithm.
    
    Algorithm Flow:
        1. Fetch the current LatestUpdate by pk
        2. Get all other LatestUpdate objects
        3. Vectorize all content using TF-IDF
        4. Calculate cosine similarity between current and all others
        5. Sort by similarity score (descending)
        6. Return top 4 most similar articles
    
    Parameters:
        request (HttpRequest): HTTP request object
        pk (int): Primary key of the LatestUpdate object
    
    Returns:
        HttpResponse: Rendered latest_update_detail.html
        404: If update not found
    
    Context:
        update (LatestUpdate): The requested blog post
        recommendations (list): Top 4 similar LatestUpdate objects
    
    ML/AI Components:
        - sklearn.feature_extraction.text.TfidfVectorizer: Text vectorization
        - sklearn.metrics.pairwise.cosine_similarity: Similarity calculation
    
    Performance Considerations:
        - Vectorization happens on every view load
        - Consider caching for large datasets
        - Top 4 limit can be adjusted
    
    URL Pattern:
        /updates/<int:pk>/
    
    Example:
        GET /updates/3/
    """
    # Retrieve the selected LatestUpdate object
    update = get_object_or_404(LatestUpdate, pk=pk)

    # Get all blog posts except the current one
    all_blogs = LatestUpdate.objects.exclude(id=pk)

    # Prepare content data for TF-IDF vectorization
    # Current update's content is first in list for similarity calculation
    blog_contents = [update.content] + [blog.content for blog in all_blogs]
    
    # Vectorize all content using TF-IDF
    vectorizer = TfidfVectorizer().fit_transform(blog_contents)
    
    # Calculate cosine similarity between current blog (index 0) and all others
    # Returns array of similarity scores [0, 1] where 1 = identical
    similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    
    # Pair each blog with its similarity score
    similar_blogs = sorted(
        zip(all_blogs, similarity_matrix),
        key=lambda x: x[1],
        reverse=True
    )[:4]  # Get top 4 recommendations

    # Extract only the blog objects (remove similarity scores)
    recommendations = [blog for blog, _ in similar_blogs]

    context = {
        'update': update, 
        'recommendations': recommendations
    }

    return render(request, 'latest_update_detail.html', context)


def featured_news_detail(request, pk):
    """
    Featured News detail view with content-based recommendations.
    
    Displays a featured news article with recommended similar articles
    using word overlap algorithm.
    
    Algorithm Flow:
        1. Fetch the FeaturedNews object by pk
        2. Extract content from linked LatestUpdate
        3. Tokenize content into unique words (lowercased)
        4. Compare word overlap with all other FeaturedNews items
        5. Score based on number of common words
        6. Return top 4 most similar articles
    
    Parameters:
        request (HttpRequest): HTTP request object
        pk (int): Primary key of the FeaturedNews object
    
    Returns:
        HttpResponse: Rendered featured_news_detail.html
        404: If featured news not found
    
    Context:
        featured (FeaturedNews): The requested featured news article
        recommendations (list): Top 4 similar FeaturedNews objects
    
    Algorithm Components:
        - regex word extraction: \w+ (alphanumeric words)
        - word set intersection: Common words between articles
        - scoring: Count of common words
    
    URL Pattern:
        /featured-news/<int:pk>/
    
    Example:
        GET /featured-news/1/
    
    Note:
        Requires LatestUpdate linked to FeaturedNews for content
    """
    # Retrieve the selected FeaturedNews object
    featured = get_object_or_404(FeaturedNews, pk=pk)
    
    # Get content from the linked LatestUpdate
    # Handle case where update might not exist
    current_content = featured.update.content if featured.update and featured.update.content else ""
    
    # Tokenize the content into unique words (lowercase for comparison)
    # \w+ matches alphanumeric word characters
    current_words = set(re.findall(r'\w+', current_content.lower()))
    
    # Fetch all other FeaturedNews items with related LatestUpdate
    # select_related optimizes query for accessing update.content
    all_blogs = FeaturedNews.objects.exclude(id=pk).select_related('update')
    recommendations = []
    
    # Calculate word overlap with other articles
    for blog in all_blogs:
        if blog.update and blog.update.content:
            # Extract words from other article
            other_words = set(re.findall(r'\w+', blog.update.content.lower()))
            # Find common words between current and other article
            common_words = current_words & other_words
            # Store blog with score (count of common words)
            recommendations.append((blog, len(common_words)))

    # Sort by number of common words (descending) and take top 4
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:4]
    # Extract only blog objects
    recommendations = [rec[0] for rec in recommendations]

    context = {
        'featured': featured, 
        'recommendations': recommendations
    }

    return render(request, 'featured_news_detail.html', context)


def open_position_list(request):
    """
    Job listings page view.
    
    Displays all open job positions in reverse chronological order
    (newest postings first).
    
    Returns:
        HttpResponse: Rendered vacancies.html
    
    Context:
        jobs (QuerySet): All OpenPosition objects ordered by posted_on
    
    URL Pattern:
        /open-positions/
    
    Example:
        GET /open-positions/
    
    Related Views:
        - open_position_detail: Shows individual job details
        - jobs_search: Search/filter job listings
    """
    jobs = OpenPosition.objects.all().order_by('-posted_on')
    return render(request, 'vacancies.html', {'jobs': jobs})


def open_position_detail(request, pk):
    """
    Individual job position detail view.
    
    Displays comprehensive job information including title, description,
    location, type, and application details.
    
    Parameters:
        request (HttpRequest): HTTP request object
        pk (int): Primary key of the OpenPosition object
    
    Returns:
        HttpResponse: Rendered open_position_detail.html
        404: If job position not found
    
    Context:
        position (OpenPosition): The requested job position
    
    URL Pattern:
        /open-positions/<int:pk>/
    
    Example:
        GET /open-positions/5/
    
    Related Views:
        - open_position_list: Shows all available jobs
    """
    position = get_object_or_404(OpenPosition, pk=pk)
    return render(request, 'open_position_detail.html', {'position': position})


class SocialMediaPostListView(ListView):
    """
    Social Media Posts list view with pagination.
    
    Displays embedded social media posts from multiple platforms
    in paginated format.
    
    Attributes:
        model (Model): SocialMediaPost model
        template_name (str): 'socialmedia_post_list.html'
        context_object_name (str): 'posts' (variable name in template)
        paginate_by (int): 5 posts per page
        ordering (list): Sort by creation date (newest first)
    
    Supported Platforms:
        - X (Twitter)
        - Instagram
        - Facebook
        - YouTube
        - LinkedIn
        - TikTok
    
    URL Pattern:
        /social-media/
    
    Template Context:
        posts (list): Paginated list of SocialMediaPost objects
        page_obj (Page): Django Page object for pagination
        is_paginated (bool): Whether list is paginated
        paginator (Paginator): Django Paginator object
    
    Example Query:
        GET /social-media/
        GET /social-media/?page=2
    
    Note:
        Embed codes are stored in code_to_embed field
        Each platform has specific embed code format
    """
    model = SocialMediaPost
    template_name = 'socialmedia_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-created']


def privacy_policy(request):
    """
    Privacy Policy page view.
    
    Static view displaying organization's privacy policy.
    
    Returns:
        HttpResponse: Rendered privacy_policy.html
    
    URL Pattern:
        /privacy_policy/
    """
    return render(request, 'privacy_policy.html')


def terms_of_use(request):
    """
    Terms of Use page view.
    
    Static view displaying website's terms and conditions.
    
    Returns:
        HttpResponse: Rendered terms_of_use.html
    
    URL Pattern:
        /terms_of_use/
    """
    return render(request, 'terms_of_use.html')


def contact_view(request):
    """
    Contact form handler.
    
    Processes contact form submissions via POST request.
    Validates form data and saves contact message.
    
    HTTP Methods:
        POST: Handle form submission
        GET: Redirects back to referrer
    
    Parameters:
        request (HttpRequest): HTTP request object
    
    Returns:
        HttpResponse: Redirect to referrer page
    
    Form Processing:
        1. Check if request method is POST
        2. Bind form data to ContactForm
        3. Validate form (checks required fields, email format)
        4. Save Contact object to database
        5. Display success message
        6. Redirect to referring page
    
    Context Messages:
        - 'Thank you! Your message has been sent.' (success)
    
    URL Pattern:
        /contact/
    
    Related Models:
        - Contact: Stores form submission data
    
    Related Forms:
        - ContactForm: Form for contact submissions
    
    Example POST Data:
        {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'I would like to inquire about...'
        }
    
    Note:
        Uses HTTP_REFERER to redirect back to submitting page
        Falls back to '/' if referrer is not available
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    
    # For GET requests, redirect back to referrer
    return redirect(request.META.get('HTTP_REFERER', '/'))


def robots_txt(request):
    """
    Robots.txt file for search engine crawlers.
    
    Provides directives for web crawlers about which pages to crawl.
    
    Returns:
        HttpResponse: Plain text robots.txt content
    
    Content:
        User-agent: * (applies to all crawlers)
        Disallow: /admin/ (prevent crawling admin pages)
        Sitemap: URL to sitemap.xml
    
    URL Pattern:
        /robots.txt
    
    Note:
        Update sitemap URL to match your domain in production
        Current URL is placeholder: https://www.example.com/sitemap.xml
    
    SEO Impact:
        - Helps search engines crawl site efficiently
        - Prevents admin/private pages from indexing
        - Directs crawlers to XML sitemap
    """
    content = "User-agent: *\nDisallow: /admin/\nSitemap: https://www.example.com/sitemap.xml"
    return HttpResponse(content, content_type="text/plain")
