from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """
    Represents a category of news or blog content on the website.

    Fields:
        category_name (CharField): The name of the category, with a maximum length of 50 characters.
        created (DateTimeField): The date and time the category was created, automatically set to the current time using timezone.now().

    Meta options:
        verbose_name: Sets the singular display name for Category objects in the admin interface to 'Category'.
        verbose_name_plural: Sets the plural display name for Category objects in the admin interface to 'Categories'.
        ordering: Orders categories by creation date in descending order (newest first).

    Methods:
        __str__(self): Returns the category name as the string representation.

    Example:
        >>> category = Category.objects.create(category_name="Tech News")
        >>> str(category)
        "Tech News"
    """

    category_name = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
    
    # def get_absolute_url(self):
        # return reverse('category_detail', kwargs={'pk': self.pk})

    

class LatestUpdate(models.Model):
    """
    Represents a single news or blog update on the website.

    This model stores blog posts, news updates, and articles with support for
    categorization, media, and content recommendations.

    Fields:
        category (ForeignKey): Reference to the Category this update belongs to.
            Deletes the update if category is deleted (CASCADE).
        title (CharField): The title of the update, max 200 characters.
        image (ImageField): Featured image for the article, uploaded to 'article_images/'.
        content (TextField): The full HTML/text content of the article.
        bullet_points (TextField): Optional semicolon-separated bullet points.
        reading_duration (CharField): Estimated reading time (e.g., '5 minutes read').
        summary (TextField): Short summary/excerpt of the article.
        author (ForeignKey): Reference to the User who created/wrote the update.
        created (DateTimeField): Auto-set to current time when created.

    Meta options:
        ordering: Orders updates by creation date (newest first).

    Methods:
        __str__(self): Returns the title.
        get_bullet_points(self): Splits bullet_points string by ';' and returns a list.
        get_absolute_url(self): Returns URL to the detail view of this update.

    Relationships:
        - Belongs to one Category
        - Written by one User (Author)
        - Can be featured as FeaturedNews
        - Used in recommendation engine for content similarity

    Example:
        >>> from muna_kalati.models import Category, LatestUpdate
        >>> from django.contrib.auth.models import User
        >>> category = Category.objects.get(pk=1)
        >>> author = User.objects.get(username='writer')
        >>> update = LatestUpdate.objects.create(
        ...     category=category,
        ...     title="New Educational Initiative",
        ...     content="Full article content here...",
        ...     author=author
        ... )
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='article_images/')
    content = models.TextField()
    bullet_points = models.TextField(blank=True, help_text="Optional bullet points for the article. Enter bullet points separated by a semicolon (;)")
    reading_duration = models.CharField(blank=True, max_length=20, default='5 minutes read')
    summary = models.TextField(verbose_name='Summary', blank=True, help_text="Optional summary of the article")
    # author = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='updates')

    created = models.DateTimeField(default=timezone.now)
    # updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created']
    #     verbose_name = 'Latest Update'
    #     verbose_name_plural = 'Latest Updates'

    def __str__(self):
        return self.title

    def get_bullet_points(self):
        """
        Split bullet points by semicolon and return as list.
        
        Returns:
            list: List of bullet point strings. Returns empty list if no bullet points.
        
        Example:
            >>> update.bullet_points = "Point 1;Point 2;Point 3"
            >>> update.get_bullet_points()
            ['Point 1', 'Point 2', 'Point 3']
        """
        if not self.bullet_points:
            return []
        return self.bullet_points.split(";")
    

    def get_absolute_url(self):
        """
        Get the absolute URL to this update's detail page.
        
        Returns:
            str: URL path to the latest_update_detail view.
        """
        return reverse('latest_update_detail', kwargs={'pk': self.pk})


class FeaturedNews(models.Model):
    """
    Represents a news article chosen to be prominently displayed on the website.

    This model links to a LatestUpdate to mark it as featured content.
    Featured articles are displayed in special sections on the homepage and media pages.

    Fields:
        update (OneToOneField): Reference to the LatestUpdate to feature.
            Cannot have duplicate featured news for the same update.
            Deletes FeaturedNews if linked update is deleted (CASCADE).
        created (DateTimeField): Auto-set to current time when created.

    Meta options:
        ordering: Orders by creation date (newest first).
        verbose_name: Singular name in admin.
        verbose_name_plural: Plural name in admin.

    Methods:
        __str__(self): Returns formatted string showing it's a featured update with title.

    Relationships:
        - Links to exactly one LatestUpdate (one-to-one)
        - One update can only be featured once at a time

    Use Cases:
        - Highlighting important announcements
        - Showcasing major news stories
        - Featured section on homepage
        - Media & news hub highlights

    Example:
        >>> update = LatestUpdate.objects.get(pk=5)
        >>> featured = FeaturedNews.objects.create(update=update)
        >>> str(featured)
        "Featured: New Educational Initiative"
    """

    update = models.OneToOneField(LatestUpdate, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(default=timezone.now)
    # updated = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Featured News'
        verbose_name_plural = 'Featured News'

    def __str__(self):
        return f"Featured: {self.update.title}" # ({self.update.created.strftime('%B %d, %Y')})


class OpenPosition(models.Model):
    """
    Represents an open job position on the website.

    This model stores job listings with details about positions, locations,
    types, and application information.

    Fields:
        job_title (CharField): The title of the position (e.g., "Software Engineer").
        brief_description (CharField): One-line description of the role, max 200 chars.
        details (TextField): Full job description, responsibilities, and requirements.
        location (CharField): Job location (e.g., "Remote", "Nairobi, Kenya", "On-site").
        job_type (CharField): Employment type (e.g., "Full-time", "Part-time", "Contract").
        posted_on (DateTimeField): Auto-set to current time when created.

    Meta options:
        ordering: Orders by posted date (newest first).

    Methods:
        __str__(self): Returns job title with formatted posting date.
        get_absolute_url(self): Returns URL to job detail page.

    Use Cases:
        - Job board/careers page
        - Job search and filtering
        - Individual job applications
        - Career growth opportunities

    Example:
        >>> job = OpenPosition.objects.create(
        ...     job_title="Content Writer",
        ...     brief_description="Create engaging Afrocentric content",
        ...     location="Remote",
        ...     job_type="Full-time"
        ... )
        >>> str(job)
        "Content Writer (Posted on June 05, 2026)"
    """

    job_title = models.CharField(max_length=200)
    brief_description = models.CharField(null=True, max_length=200)
    details = models.TextField(null=True, help_text='Job details')
    posted_on = models.DateTimeField(null=True, auto_now_add=True)
    location = models.CharField(null=True, max_length=100, help_text='Remote, On-site, etc')
    job_type = models.CharField(default='', max_length=100, help_text='Full-time, Part-time, etc')

    class Meta:
        # verbose_name_plural = "Open Positions"      
        ordering = ['-posted_on']

    def __str__(self):
        return f"{self.job_title} (Posted on {self.posted_on.strftime('%B %d, %Y')})"
    

    def get_absolute_url(self):
        """
        Get the absolute URL to this position's detail page.
        
        Returns:
            str: URL path to the job_details view.
        """
        return reverse('job_details', kwargs={'pk': self.pk})


class ExternalMediaContent(models.Model):
    """
    Represents external media content from third-party sources.

    This model stores references to media content (articles, videos, etc.)
    from external sources like news outlets, publications, or partner sites.

    Fields:
        title (CharField): Title of the external content, max 255 characters.
        source (CharField): Name of the source/publication, max 255 characters.
        source_icon (FileField): Logo/icon of the source, uploaded to 'source_icons/'.
            Optional field, useful for branding in UI.
        image (ImageField): Featured image/thumbnail, uploaded to 'media_images/'.
        link (URLField): Direct URL to the external content.
        created (DateTimeField): Auto-set to current time when content is added.

    Meta options:
        ordering: Orders by creation date (newest first).

    Methods:
        __str__(self): Returns the content title.

    Use Cases:
        - Media mentions and press coverage
        - Featured articles from partners
        - News aggregation
        - Social media content links
        - Press coverage tracking

    Example:
        >>> media = ExternalMediaContent.objects.create(
        ...     title="Muna Kalati Featured in BBC",
        ...     source="BBC News",
        ...     image="path/to/image.jpg",
        ...     link="https://www.bbc.com/news/article"
        ... )
        >>> str(media)
        "Muna Kalati Featured in BBC"
    """
    
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    source_icon = models.FileField(upload_to='source_icons/', null=True, blank=True)
    image = models.ImageField(upload_to='media_images/')
    link = models.URLField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        """
        Returns a string representation of the ExternalMediaContent object, using its title.

        Returns:
            str: The title of the ExternalMediaContent object.
        """
        return self.title


class PressRelease(models.Model):
    """
    Represents an official press release from the organization.

    This model stores press releases which are formal announcements about
    organizational news, initiatives, partnerships, or important updates.

    Fields:
        title (CharField): The title of the press release, max 200 characters.
        content (TextField): The full text content of the press release.
        created (DateTimeField): Auto-set to current time when created.

    Meta options:
        ordering: Orders by creation date (newest first).

    Methods:
        __str__(self): Returns the press release title.
        get_absolute_url(self): Returns URL to the detail view.

    Use Cases:
        - Official announcements
        - Partnership announcements
        - Milestone celebrations
        - Product/feature launches
        - Organizational news
        - Media kit resources

    Note:
        Press releases differ from blog posts (LatestUpdate) by being
        more formal and official communications.

    Example:
        >>> press = PressRelease.objects.create(
        ...     title="Muna Kalati Launches in 39 African Languages",
        ...     content="Today we are proud to announce..."
        ... )
        >>> str(press)
        "Muna Kalati Launches in 39 African Languages"
    """

    title = models.CharField(max_length=200)
    # image = models.ImageField(upload_to='article_images/', blank=True)
    content = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    # updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created'] 

    def __str__(self):
        """
        Returns a string representation of the PressRelease object, using its title.

        Returns:
            str: The title of the PressRelease object.
        """
        return self.title
    

    def get_absolute_url(self):
        """
        Get the absolute URL to this press release's detail page.
        
        Returns:
            str: URL path to the press_release_detail view.
        """
        return reverse('press_release_detail', kwargs={'pk': self.pk})
    

class SocialMediaPost(models.Model):
    """
    Represents an embedded social media post from various platforms.

    This model stores embed codes and metadata for social media posts
    that are displayed on the website from platforms like X, Instagram, etc.

    Fields:
        platform (CharField): The social media platform.
            Choices: 'x', 'instagram', 'facebook', 'youtube', 'linkedin', 'tiktok'
        code_to_embed (TextField): The embed code or iframe HTML from the platform.
            Can also be used for descriptions or captions.
        created (DateTimeField): Auto-set to current time when post is added.

    Meta options:
        ordering: Orders by creation date (newest first).

    Platform Choices:
        - 'x' (formerly Twitter): X.com posts
        - 'instagram': Instagram posts and reels
        - 'facebook': Facebook posts and videos
        - 'youtube': YouTube videos
        - 'linkedin': LinkedIn posts and articles
        - 'tiktok': TikTok videos

    Use Cases:
        - Displaying social media feeds
        - Sharing viral content
        - Showcasing community engagement
        - Cross-platform content strategy
        - Social proof and testimonials

    Implementation Notes:
        - Store the embed code provided by each platform's embed/share feature
        - Each platform has different embed code formats
        - Update embed codes periodically as platform formats change

    Example:
        >>> post = SocialMediaPost.objects.create(
        ...     platform='x',
        ...     code_to_embed='<blockquote class="twitter-tweet">...</blockquote>'
        ... )
        >>> str(post)
        "X (Posted on June 05, 2026)"
    """
    
    PLATFORM_CHOICES = [
        ('x', 'X'),
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('tiktok', 'TikTok'),
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    code_to_embed = models.TextField(blank=True, null=True, help_text="Optional description or caption for the post")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        """
        Returns the platform name and creation date.
        
        Returns:
            str: Platform display name with creation date.
        """
        return f"{self.get_platform_display()} (Posted on {self.created.strftime('%B %d, %Y')})"


class Contact(models.Model):
    """
    Represents a contact form submission from website visitors.

    This model captures messages from the public contact form, enabling
    the organization to respond to inquiries and feedback.

    Fields:
        name (CharField): Full name of the person submitting the form, max 100 chars.
        email (EmailField): Email address for response and contact.
        message (TextField): The message or inquiry content.
        date (DateTimeField): Auto-set to current time when submitted.

    Meta options:
        ordering: Orders by date in descending order (newest first).
        verbose_name_plural: "Contact Messages"

    Methods:
        __str__(self): Returns name and email for identification.

    Use Cases:
        - Visitor inquiries and support requests
        - Partnership proposals
        - Content submissions
        - Feedback and suggestions
        - Media inquiries

    Recommendations:
        - Regularly review and respond to submissions
        - Consider adding email notifications for new submissions
        - Archive old messages periodically
        - Implement spam filtering/validation

    Example:
        >>> contact = Contact.objects.create(
        ...     name="Jane Doe",
        ...     email="jane@example.com",
        ...     message="I would like to partner with Muna Kalati..."
        ... )
        >>> str(contact)
        "Jane Doe - jane@example.com"
    """
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.email}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Contact Messages"


class HeroSection(models.Model):
    """
    Represents the hero/banner section displayed at the top of the homepage.

    This model manages the main hero section with header text, background imagery,
    and optional video for maximum visual impact on landing pages.

    Fields:
        header_text (CharField): Main heading text for the hero section, max 200 chars.
            Optional, allows for dynamic hero content.
        background_image (ImageField): Hero section background image.
            Uploaded to 'hero_images/', optional, can use CSS fallback.
        banner_video (FileField): Hero section background video (mp4, webm, etc).
            Uploaded to 'hero_images/', optional, for modern video backgrounds.

    Meta options:
        verbose_name: "Hero Section" (singular)
        verbose_name_plural: "Hero Section" (singular, only one should exist)

    Design Pattern:
        This model typically has only ONE instance in production.
        It represents the global hero section visible to all users.

    Use Cases:
        - Homepage hero banner
        - Main landing page visual
        - Call-to-action section
        - Brand messaging display

    Best Practices:
        - Keep at most one HeroSection instance
        - Use high-quality, optimized images
        - Provide both image and video alternatives
        - Ensure text is readable over background
        - Test on mobile devices

    Example:
        >>> hero = HeroSection.objects.create(
        ...     header_text="Empowering African Children Through Afrocentric Education",
        ...     background_image="path/to/hero.jpg"
        ... )
        >>> hero_latest = HeroSection.objects.last()
    """
    
    header_text = models.CharField(null=True, blank=True, max_length=200)
    background_image = models.ImageField(null=True, blank=True, upload_to='hero_images/', help_text="Optional banner image")
    banner_video = models.FileField(null=True, blank=True, upload_to='hero_images/', help_text="Optional banner video")
    # button_text = models.CharField(max_length=50, default="Learn More")
    # button_link = models.URLField(default="/features")

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return "Hero Section"


class TeamMember(models.Model):
    """
    Represents a member of the organization's team.

    This model stores information about team members for display on
    the team/about page, including their bio and social media profiles.

    Fields:
        name (CharField): Full name of the team member, max 100 characters.
        title (CharField): Job title or position, max 100 characters.
            (e.g., "Founder & CEO", "Content Director")
        bio (TextField): Professional biography or background information.
        image (ImageField): Profile picture/headshot, uploaded to 'images/team/'.
        linkedin_url (URLField): LinkedIn profile URL (optional).
        facebook_url (URLField): Facebook profile URL (optional).
        instagram_url (URLField): Instagram profile URL (optional).
        x_url (URLField): X (Twitter) profile URL (optional).

    Meta options:
        ordering: Orders by name alphabetically.
        verbose_name_plural: "Team Members"

    Methods:
        __str__(self): Returns the team member's name.

    Use Cases:
        - Team/about page display
        - Leadership team showcase
        - Staff directory
        - Contributor recognition
        - Team culture highlighting

    Best Practices:
        - Use professional headshots
        - Keep bios concise but informative
        - Include relevant social media profiles
        - Update when team changes
        - Order by leadership hierarchy

    Example:
        >>> member = TeamMember.objects.create(
        ...     name="Kofi Mensah",
        ...     title="Founder & CEO",
        ...     bio="Passionate about African education...",
        ...     image="path/to/kofi.jpg",
        ...     linkedin_url="https://linkedin.com/in/kofi"
        ... )
        >>> str(member)
        "Kofi Mensah"
    """
    
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='images/team/')
    linkedin_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    x_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Team Members"


class UserProfile(models.Model):
    """
    Extended user profile for additional user information.

    This model extends Django's built-in User model with additional
    fields for professional information and profile customization.

    Fields:
        user (OneToOneField): Reference to Django's User model.
            Each User can have exactly one UserProfile.
            Deletes profile if user is deleted (CASCADE).
        title (CharField): Professional title or role, max 100 chars (optional).
        profile_picture (ImageField): User's profile picture/avatar (optional).
            Uploaded to 'profile_pictures/'.
        linkedin_url (URLField): LinkedIn profile URL (optional).

    Meta options:
        ordering: Default ordering
        verbose_name_plural: "User Profiles"

    Methods:
        __str__(self): Returns "{username}'s profile" format.

    Use Cases:
        - User profile pages
        - Author profiles on blog posts
        - Staff directory extensions
        - User account customization
        - Professional information storage

    Related Models:
        - User (Django's auth model)
        - Related via reverse relation: user.profile

    Access Pattern:
        >>> user = User.objects.get(username='john_doe')
        >>> profile = user.profile  # Access via reverse relation
        >>> profile.title
        "Senior Content Manager"

    Example:
        >>> from django.contrib.auth.models import User
        >>> user = User.objects.create_user(username='jane', email='jane@example.com')
        >>> profile = UserProfile.objects.create(
        ...     user=user,
        ...     title="Content Writer",
        ...     linkedin_url="https://linkedin.com/in/jane"
        ... )
        >>> str(profile)
        "jane's profile"
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"

    class Meta:
        verbose_name_plural = "User Profiles"


class Review(models.Model):
    """
    Represents a customer/user review or testimonial.

    This model stores reviews and ratings from users, visitors, or customers
    about the organization or its services/products.

    Fields:
        name (CharField): Reviewer's name, max 100 characters.
        role (CharField): Reviewer's role/position/company, max 100 characters.
            (e.g., "Teacher", "Parent", "School Administrator")
        review_text (TextField): The full review or testimonial text.
        rating (DecimalField): Star rating from 3.5 to 5.0 in 0.5 increments.
            Range: 3.5, 4.0, 4.5, 5.0 (representing half-star intervals)

    Choices:
        RATING_CHOICES: [(3.5, '3.5'), (4.0, '4.0'), (4.5, '4.5'), (5.0, '5.0')]

    Meta options:
        ordering: Orders by rating (highest first).
        verbose_name_plural: "Reviews & Testimonials"

    Methods:
        __str__(self): Returns "{name} - {rating} Stars" format.

    Use Cases:
        - Testimonials on about/home page
        - Social proof for credibility
        - User feedback display
        - Rating aggregation
        - Case studies and success stories

    Rating Scale:
        - 3.5 stars: Good
        - 4.0 stars: Very Good
        - 4.5 stars: Excellent
        - 5.0 stars: Outstanding

    Best Practices:
        - Verify reviews before publishing
        - Feature highest-rated reviews prominently
        - Respond to all reviews (especially 5-star)
        - Update testimonial page regularly
        - Consider geographic/role diversity

    Example:
        >>> review = Review.objects.create(
        ...     name="Amina Okonkwo",
        ...     role="Primary School Teacher",
        ...     review_text="Muna Kalati has transformed how I teach African history...",
        ...     rating=5.0
        ... )
        >>> str(review)
        "Amina Okonkwo - 5.0 Stars"
    """
    
    RATING_CHOICES = [(i * 0.5, str(i * 0.5)) for i in range(7, 11)] # 3.5 to 5.0 in 0.5 intervals

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.DecimalField(choices=RATING_CHOICES, max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.name} - {self.rating} Stars"

    class Meta:
        ordering = ['-rating']
        verbose_name_plural = "Reviews & Testimonials"



# google-site-verification=F7BAZujZ3i01ED0wn6ScipWsdOAUzaEVSwqaHL2s6ro
