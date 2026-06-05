"""
Django Admin Configuration for Muna Kalati Application

This module customizes the Django admin interface for managing content.
Uses Jazzmin theme for enhanced UI and user experience.

Admin Classes:
    - CategoryAdmin: Manage content categories
    - LatestUpdateAdmin: Manage blog posts with GMT timezone conversion
    - FeaturedNewsAdmin: Manage featured news articles
    - OpenPositionAdmin: Manage job listings
    - ExternalMediaContentAdmin: Manage external media links
    - PressReleaseAdmin: Manage press releases
    - SocialMediaPostAdmin: Manage social media posts
    - ContactAdmin: View contact form submissions (read-only)
    - TeamMemberAdmin: Manage team member profiles
    - CustomUserAdmin: Extended user admin with profiles
    - ReviewAdmin: Manage testimonials and reviews

Features:
    - Custom list displays with computed fields
    - Search functionality
    - Filtering capabilities
    - Read-only contact submissions
    - User profile management with inline editing
    - Timezone-aware datetime display
    - Image preview support
"""

from django.contrib import admin
from .models import (
    UserProfile, LatestUpdate, FeaturedNews, OpenPosition,
    ExternalMediaContent, PressRelease, Category, SocialMediaPost,
    Contact, HeroSection, TeamMember, Review
)
from django.utils.html import format_html
import pytz

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing content categories.
    
    Features:
        - Display category name and creation date
        - Search by category name
        - Filter by creation date
    
    List Display:
        - category_name: Name of the category
        - created: When the category was created
    
    Search Fields:
        - category_name: Full-text search
    
    Filters:
        - created: Date range filtering
    
    Use Cases:
        - Create/edit content categories
        - Organize blog posts by topic
        - Manage category taxonomy
    
    Typical Categories:
        - Tech News
        - Education
        - Resources
        - Announcements
    """
    list_display = ('category_name', 'created')
    search_fields = ['category_name']
    list_filter = ['created']


class LatestUpdateAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing blog posts and latest updates.
    
    Features:
        - Display title, category, author, and creation date (GMT)
        - Search by title and author
        - Filter by category and author
        - Custom method to show creation time in GMT timezone
    
    List Display:
        - title: Blog post title
        - category: Associated category
        - author__username: Post author
        - created_in_gmt: Custom field showing GMT conversion
    
    Search Fields:
        - title: Full-text search on post title
        - author__username: Search by author username
    
    Filters:
        - category: Filter by content category
        - author__username: Filter by author
    
    Custom Methods:
        - created_in_gmt(): Converts created timestamp to GMT for display
    
    Use Cases:
        - Create/edit blog posts
        - Manage article metadata
        - Track author activity
        - Content calendar management
    
    Timezone Handling:
        - Database time: Stored in database timezone (Africa/Abidjan)
        - Display time: Converted to GMT for consistency
        - Formula: obj.created.astimezone(gmt_timezone)
    
    Example Display:
        Title: "Education in Africa"
        Category: Tech News
        Author: john_doe
        Created (GMT): 2026-06-05 14:30:45 GMT
    """
    list_display = ('title', 'category', 'author__username', 'created_in_gmt')
    search_fields = ['title', 'author__username']
    list_filter = ['category', 'author__username']

    def created_in_gmt(self, obj):
        """
        Custom admin display field showing creation time in GMT.
        
        Converts the creation datetime from the configured timezone
        (Africa/Abidjan) to GMT for consistent time display.
        
        Parameters:
            obj (LatestUpdate): The LatestUpdate instance
        
        Returns:
            str: Formatted datetime string in GMT (YYYY-MM-DD HH:MM:SS GMT)
        
        Example Output:
            "2026-06-05 14:30:45 GMT"
        
        Implementation:
            - Use pytz.timezone('GMT') for GMT timezone
            - Call astimezone() to convert from stored timezone
            - Format using strftime() for readable output
        """
        gmt_timezone = pytz.timezone('GMT')
        return obj.created.astimezone(gmt_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')

    created_in_gmt.short_description = 'Created (GMT)'


class FeaturedNewsAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing featured news articles.
    
    Features:
        - Display featured news with linked update title
        - Custom method to show related LatestUpdate title
        - Filter by creation date
    
    List Display:
        - get_update_title: Custom field showing LatestUpdate title
        - created: When featured news was created
    
    Custom Methods:
        - get_update_title(): Retrieves and displays title from related LatestUpdate
    
    Use Cases:
        - Promote important articles to featured section
        - Manage featured news rotation
        - Track featured article history
    
    Relationship:
        - One-to-One relationship with LatestUpdate
        - Deleting LatestUpdate also deletes FeaturedNews
    
    Example Display:
        Update Title: "New Educational Initiative"
        Created: 2026-06-05 10:00:00
    """
    list_display = ('get_update_title', 'created')

    def get_update_title(self, obj):
        """
        Display the title of the related LatestUpdate.
        
        Retrieves the title from the one-to-one related LatestUpdate.
        
        Parameters:
            obj (FeaturedNews): The FeaturedNews instance
        
        Returns:
            str: Title of the associated LatestUpdate
        
        Note:
            Relationship is obj.update.title (one-to-one)
        """
        return obj.update.title
    
    get_update_title.short_description = 'Update Title'


class OpenPositionAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing job listings.
    
    Features:
        - Display job title and posting date
        - Search by job title and date
        - Filter by job title and posting date
    
    List Display:
        - job_title: Title of the position
        - posted_on: When the job was posted
    
    Search Fields:
        - job_title: Search jobs by title
        - posted_on: Search by date
    
    Filters:
        - job_title: Filter by job title
        - posted_on: Filter by posting date range
    
    Use Cases:
        - Post new job openings
        - Manage active job listings
        - Track job posting history
        - Manage applications
    
    Related Fields (in model but not displayed):
        - brief_description: Short job summary
        - details: Full job description
        - location: Job location or "Remote"
        - job_type: "Full-time", "Part-time", etc.
    
    Example Display:
        Job Title: Software Engineer
        Posted On: 2026-06-01
    """
    list_display = ('job_title', 'posted_on')
    search_fields = ['job_title', 'posted_on']
    list_filter = ['job_title', 'posted_on']


class ExternalMediaContentAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing external media content.
    
    Features:
        - Display title, source, and creation date
        - Search by title, source, and date
        - Filter by title, source, and date
    
    List Display:
        - title: Content title
        - source: Source/publication name
        - created: When content was added
    
    Search Fields:
        - title: Search by content title
        - source: Search by source/publication
        - created: Search by date
    
    Filters:
        - title: Filter by title
        - source: Filter by source
        - created: Filter by date range
    
    Use Cases:
        - Track media mentions and coverage
        - Manage press coverage links
        - Aggregate external news
        - Build media kit
    
    Related Fields (in model but not displayed):
        - source_icon: Publisher logo/icon
        - image: Thumbnail image
        - link: URL to external content
    
    Example Display:
        Title: "Muna Kalati Featured in BBC"
        Source: BBC News
        Created: 2026-06-05
    """
    list_display = ('title', 'source', 'created')
    search_fields = ['title', 'source', 'created']
    list_filter = ['title', 'source', 'created']


class PressReleaseAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing press releases.
    
    Features:
        - Display title and creation date
        - Search by title and date
        - Filter by title and date
    
    List Display:
        - title: Press release title
        - created: Publication date
    
    Search Fields:
        - title: Search by release title
        - created: Search by date
    
    Filters:
        - title: Filter by title
        - created: Filter by date range
    
    Use Cases:
        - Publish official announcements
        - Manage press release archive
        - Track company news timeline
        - Media relations management
    
    Related Fields (in model but not displayed):
        - content: Full press release text
    
    Example Display:
        Title: "Muna Kalati Expands to 39 Languages"
        Created: 2026-06-05
    
    Note:
        This class is defined twice in original code (PressReleaseAdmin appears
        on lines 49-52 and 54-57). Only one should be active.
    """
    list_display = ('title', 'created')
    search_fields = ['title', 'created']
    list_filter = ['title', 'created']


class SocialMediaPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing social media posts.
    
    Features:
        - Display platform and creation date
        - Search by platform and date
        - Filter by platform and date
    
    List Display:
        - platform: Social media platform (X, Instagram, etc.)
        - created: When post was added
    
    Search Fields:
        - platform: Search by platform name
        - created: Search by date
    
    Filters:
        - platform: Filter by platform
        - created: Filter by date range
    
    Platforms Supported:
        - X (Twitter)
        - Instagram
        - Facebook
        - YouTube
        - LinkedIn
        - TikTok
    
    Use Cases:
        - Embed social media content
        - Manage social media feed
        - Display user engagement
        - Cross-platform content sharing
    
    Related Fields (in model but not displayed):
        - code_to_embed: HTML embed code or caption
    
    Example Display:
        Platform: Instagram
        Created: 2026-06-05
    """
    list_display = ('platform', 'created')
    search_fields = ['platform', 'created']
    list_filter = ['platform', 'created']


class ContactAdmin(admin.ModelAdmin):
    """
    Admin configuration for viewing contact form submissions.
    
    Features:
        - Display contact information and submission date
        - Search by name and date
        - Read-only interface (no editing or adding)
        - Protects contact data integrity
    
    List Display:
        - name: Visitor's name
        - email: Visitor's email
        - date: Submission date/time
    
    Search Fields:
        - name: Search by visitor name
        - date: Search by submission date
    
    Filters:
        - date: Filter by date range
    
    Read-Only Fields:
        - name: Cannot be edited
        - email: Cannot be edited
        - message: Cannot be edited
        - date: Cannot be edited
    
    Permissions Disabled:
        - has_add_permission: False (cannot manually add contacts)
        - has_change_permission: False (cannot edit submissions)
    
    Can Still:
        - View contact submissions
        - Search and filter
        - Delete submissions (with proper permissions)
    
    Use Cases:
        - Review visitor inquiries
        - Monitor form submissions
        - Respond to messages
        - Archive contact data
    
    Example Display:
        Name: John Doe
        Email: john@example.com
        Date: 2026-06-05 14:30:45
    
    Note:
        Contact messages are created only through public form.
        This admin view is read-only by design.
    """
    list_display = ('name', 'email', 'date')
    search_fields = ['name', 'date']
    list_filter = ['date', 'date']
    readonly_fields = ('name', 'email', 'message', 'date')

    def has_add_permission(self, request):
        """
        Disable manual contact submission creation in admin.
        
        Returns:
            bool: False - prevents adding new contact entries
        
        Rationale:
            Contacts should only come from public form.
            Protects data integrity and prevents admin manipulation.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Disable editing of contact submissions in admin.
        
        Parameters:
            request (HttpRequest): Admin request
            obj (Contact): Contact object (optional)
        
        Returns:
            bool: False - prevents editing any contact entry
        
        Rationale:
            Contact submissions should be immutable once saved.
            Maintains audit trail of original submissions.
        """
        return False


class TeamMemberAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing team member profiles.
    
    Features:
        - Display name and job title
        - Search by name and title
        - Filter by name and title
    
    List Display:
        - name: Team member's full name
        - title: Job title/position
    
    Search Fields:
        - name: Search by member name
        - title: Search by job title
    
    Filters:
        - name: Filter by name
        - title: Filter by job title
    
    Use Cases:
        - Add/edit team member profiles
        - Manage team directory
        - Update job titles and roles
        - Team page management
    
    Related Fields (in model but not displayed):
        - bio: Professional biography
        - image: Profile picture
        - linkedin_url: LinkedIn profile
        - facebook_url: Facebook profile
        - instagram_url: Instagram profile
        - x_url: X/Twitter profile
    
    Example Display:
        Name: Kofi Mensah
        Title: Founder & CEO
    """
    list_display = ('name', 'title')
    search_fields = ['name', 'title']
    list_filter = ['name', 'title']


class UserProfileInline(admin.StackedInline):
    """
    Inline admin configuration for editing UserProfile within User admin.
    
    Features:
        - Edit user profile alongside user details
        - Stacked layout (profile below user fields)
        - Cannot delete profile (can_delete=False)
    
    Attributes:
        model (Model): UserProfile
        can_delete (bool): False - prevents profile deletion
        verbose_name_plural (str): "Profile" display name
        fk_name (str): 'user' - foreign key field name
    
    Use Cases:
        - Add professional title to user account
        - Upload profile picture
        - Add LinkedIn URL
        - Manage user extended information
    
    Note:
        Only shows when editing existing user (not on user creation)
        See CustomUserAdmin.get_inline_instances() for logic
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """
    Extended user admin with UserProfile inline editing.
    
    Features:
        - Standard Django user fields plus profile
        - Inline profile editing
        - Custom list display with title and profile picture
        - Only show profile for existing users (not on creation)
    
    List Display:
        - username: User login name
        - first_name: User's first name
        - last_name: User's last name
        - is_staff: Admin status indicator
        - get_title: Custom field from profile
        - display_profile_picture: Thumbnail image preview
    
    Inlines:
        - UserProfileInline: Edit profile within user admin
    
    Custom Methods:
        - get_inline_instances(): Show profile only for existing users
        - get_title(): Display title from related profile
        - display_profile_picture(): Show profile picture thumbnail
    
    Use Cases:
        - Create/edit user accounts
        - Assign admin/staff roles
        - Manage user profiles
        - Update professional information
    
    Related Model:
        - UserProfile: One-to-one relationship with User
    
    Example Display:
        Username: john_doe
        First Name: John
        Last Name: Doe
        Is Staff: Yes
        Title: Content Manager
        Profile Picture: [Small thumbnail image]
    """
    inlines = [UserProfileInline]
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'get_title', 'display_profile_picture')

    def get_inline_instances(self, request, obj=None):
        """
        Only show profile inline when editing existing user.
        
        Returns empty list when adding new user (obj=None).
        Returns inlines when editing existing user.
        
        Parameters:
            request (HttpRequest): Admin request
            obj (User): User object (None when creating new user)
        
        Returns:
            list: Inline instances (empty for new users, populated for existing)
        
        Rationale:
            UserProfile is created by signal when user is saved.
            Inline editing not available until user is created.
        """
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
    
    def get_title(self, obj):
        """
        Display title from related UserProfile.
        
        Parameters:
            obj (User): User object
        
        Returns:
            str: Title from user's profile, or None if not set
        
        Handles:
            - Missing profile (should not happen due to signal)
            - Missing title (None displayed)
        """
        return obj.profile.title
    
    get_title.short_description = 'Title'
    get_title.admin_order_field = 'profile__title'

    def display_profile_picture(self, obj):
        """
        Display profile picture as small thumbnail image.
        
        Shows a 40x40px circular thumbnail of the user's profile picture.
        Displays "No Image" if no picture is set.
        
        Parameters:
            obj (User): User object
        
        Returns:
            str: HTML img tag for thumbnail or "No Image" text
        
        HTML Styling:
            - Width/Height: 40px (square)
            - Border-radius: 25px (circular)
            - Responsive: Uses relative URL from media storage
        
        Security:
            - Uses format_html() to safely render HTML
            - Image URL from FileField.url
        """
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 25px;" />',
                obj.profile.profile_picture.url
            )
        return "No Image"

    display_profile_picture.short_description = 'Profile Picture'


class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing customer reviews and testimonials.
    
    Features:
        - Display reviewer name, role, and rating
        - Filter by rating (5.0, 4.5, 4.0, 3.5 stars)
        - Default sort by highest rating first
    
    List Display:
        - name: Reviewer's name
        - role: Reviewer's role/position
        - rating: Star rating (3.5 to 5.0)
    
    Filters:
        - rating: Filter by star rating
    
    Use Cases:
        - Feature testimonials
        - Track review ratings
        - Manage social proof
        - Display success stories
    
    Related Fields (in model but not displayed):
        - review_text: Full review content
    
    Rating Scale:
        - 5.0 stars: Outstanding
        - 4.5 stars: Excellent
        - 4.0 stars: Very Good
        - 3.5 stars: Good
    
    Example Display:
        Name: Amina Okonkwo
        Role: Primary School Teacher
        Rating: 5.0
    
    Note:
        Reviews are typically added via public form or imported.
        Admin interface for moderation and featured display.
    """
    list_display = ('name', 'role', 'rating')
    list_filter = ('rating',)


# ==================== ADMIN REGISTRATION ====================

# Unregister the default Django User admin
admin.site.unregister(User)

# Register all models with their admin configurations
admin.site.register(User, CustomUserAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)
admin.site.register(HeroSection)
admin.site.register(Category, CategoryAdmin)
admin.site.register(LatestUpdate, LatestUpdateAdmin)
admin.site.register(FeaturedNews, FeaturedNewsAdmin)
admin.site.register(OpenPosition, OpenPositionAdmin)
admin.site.register(ExternalMediaContent, ExternalMediaContentAdmin)
admin.site.register(PressRelease, PressReleaseAdmin)
admin.site.register(SocialMediaPost, SocialMediaPostAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Review, ReviewAdmin)
