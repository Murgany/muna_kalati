from django.shortcuts import render,  get_object_or_404, redirect
from django.views.generic import ListView
from .models import HeroSection, LatestUpdate, FeaturedNews, OpenPosition, ExternalMediaContent, PressRelease, SocialMediaPost, Category, TeamMember
import time
from django.db.models import Q
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib import messages
from .forms import ContactForm
import re


def updates_search(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    filters = Q()
    
    if query:
        filters |= (Q(title__icontains=query) | 
                    Q(bullet_points__icontains=query) | 
                    Q(content__icontains=query) | 
                    Q(summary__icontains=query))
    
    if category_id:
        filters &= Q(category_id=category_id)

    latest_updates = LatestUpdate.objects.filter(filters).order_by('-id')
    
    context = {
        'latest_updates': latest_updates,
        'query': query,
        'categories': Category.objects.all(),  # Ensure categories are available for the dropdown
    }
    
    return render(request, 'search_results.html', context)


def jobs_search(request):
    query = request.GET.get('q')
    if query:
        jobs = OpenPosition.objects.filter(Q(job_title__icontains=query) | Q(brief_description__icontains=query) | Q(details__icontains=query) | Q(job_type__icontains=query) | Q(job_type__icontains=query)).order_by('-id')

        context = {
            'jobs': jobs,
            'query': query,
        }
    else:
        context = {}
    return render(request, 'search_results.html', context)


def index(request):
    """
    Home page view.

    Returns:
        HttpResponse: The rendered homepage.
    """
    hero_section = HeroSection.objects.last()  
    return render(request, 'index.html', {'hero_section': hero_section})


def about_us(requrst):
    team_members = TeamMember.objects.all().order_by('-id')
    return render(requrst, 'about_us.html', {'team_members': team_members})


def features(request):
    img_name = None
    img_name = f'qr_{time.time()}.png'
    return render(request, 'features.html', {'img_name': img_name})


def media_and_news(request):
    """
    Combined view for displaying all latest updates and featured news.
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
    Detail view for a single latest update.
    """
    release = get_object_or_404(PressRelease, pk=pk)
    return render(request, 'press_release_detail.html', {'release': release})


class LatestUpdateListView(ListView):
    model = LatestUpdate
    template_name = 'latest_update_list.html'
    context_object_name = 'latest_updates'
    paginate_by = 8  # Number of updates per page, can be customized

    def get_context_data(self, **kwargs):
        # Custom context for further customization in the template
        context = super().get_context_data(**kwargs)
        return context


def latest_update_detail(request, pk):
    """
    Detail view for a single latest update.
    """
    update = get_object_or_404(LatestUpdate, pk=pk)

    # Get the current blog post
    # current_blog = get_object_or_404(LatestUpdate, pk=pk)

    # Get all blogs from the database
    all_blogs = LatestUpdate.objects.exclude(id=pk)  # exclude current blog

    # Prepare content data for TF-IDF
    blog_contents = [update.content] + [blog.content for blog in all_blogs]
    vectorizer = TfidfVectorizer().fit_transform(blog_contents)
    
    # Calculate cosine similarity between current blog and all others
    similarity_matrix = cosine_similarity(vectorizer[0:1], vectorizer[1:]).flatten()
    
    # Pair each similarity score with its blog entry
    similar_blogs = sorted(
        zip(all_blogs, similarity_matrix),
        key=lambda x: x[1],
        reverse=True
    )[:4]  # Get top 4 recommendations

    # Extract only the blog objects for the template
    recommendations = [blog for blog, _ in similar_blogs]

    context = {
        'update': update, 
        'recommendations': recommendations
        }

    return render(request, 'latest_update_detail.html', context)


def featured_news_detail(request, pk):
    # Retrieve the selected FeaturedNews object by its primary key (pk)
    featured = get_object_or_404(FeaturedNews, pk=pk)
    
    # Get the content from the linked LatestUpdate for this FeaturedNews
    current_content = featured.update.content if featured.update and featured.update.content else ""
    
    # Tokenize the current content to identify unique words
    current_words = set(re.findall(r'\w+', current_content.lower()))
    
    # Fetch all other FeaturedNews items for recommendations
    all_blogs = FeaturedNews.objects.exclude(id=pk).select_related('update')
    recommendations = []
    
    # Calculate word overlap with other articles
    for blog in all_blogs:
        if blog.update and blog.update.content:
            other_words = set(re.findall(r'\w+', blog.update.content.lower()))
            common_words = current_words & other_words
            recommendations.append((blog, len(common_words)))

    # Sort recommendations by the number of common words (descending) and take the top 4
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)[:4]
    recommendations = [rec[0] for rec in recommendations]

    # Pass the featured article and recommendations to the template
    context = {
        'featured': featured, 
        'recommendations': recommendations
    }

    return render(request, 'featured_news_detail.html', context)


# OpenPosition Views
def open_position_list(request):
    """
    List view for displaying all open positions.
    """
    jobs = OpenPosition.objects.all().order_by('-posted_on')
    return render(request, 'vacancies.html', {'jobs': jobs})


def open_position_detail(request, pk):
    """
    Detail view for a single open position.
    """
    position = get_object_or_404(OpenPosition, pk=pk)
    return render(request, 'open_position_detail.html', {'position': position})


# List all social media posts with pagination
class SocialMediaPostListView(ListView):
    model = SocialMediaPost
    template_name = 'socialmedia_post_list.html'  # Customize the template path
    context_object_name = 'posts'  # Optional, defaults to object_list
    paginate_by = 5  # Number of posts per page
    ordering = ['-created']  # Ensures posts are ordered by creation date


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_use(request):
    return render(request, 'terms_of_use.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect(request.META.get('HTTP_REFERER', '/'))
