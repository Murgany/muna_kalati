from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Represents a category of news or blog content on the website.

    Fields:
        category_name (CharField): The name of the category, with a maximum length of 50 characters.
        created (DateTimeField): The date and time the category was created, automatically set to the current time using timezone.now().

    Meta options:
        verbose_name: Sets the singular display name for Category objects in the admin interface to 'Category'.
        verbose_name_plural: Sets the plural display name for Category objects in the admin interface to 'Categories'.

    Methods:
        __str__(self): Returns a string representation of the Category object, using its name.
    """

    category_name = models.CharField(max_length=50)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name
    

class LatestUpdate(models.Model):
    """
    Represents a single news or blog update on the website.

    Fields:
        title (CharField): The title of the update, with a maximum length of 200 characters.
        image (ImageField): An image associated with the update, uploaded to the 'article_images/' folder.
        content (TextField): The detailed content of the update, formatted as text.
        created (DateTimeField): The date and time the update was created, automatically set to the current time using timezone.now().
        updated_at (DateTimeField): The date and time the update was last modified, automatically set to the current time using timezone.now().

    Meta options:
        ordering: Orders LatestUpdate objects by their created in descending order, displaying the most recent updates first.
        verbose_name: Sets the singular display name for LatestUpdate objects in the admin interface to 'Latest Update'.
        verbose_name_plural: Sets the plural display name for LatestUpdate objects in the admin interface to 'Latest Updates'.

    Methods:
        __str__(self): Returns a string representation of the LatestUpdate object, using its title.
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
        # Split the bullet points string by semicolon into a list
        return self.bullet_points.split(";")


class FeaturedNews(models.Model):
    """
    Represents a single news article chosen to be prominently displayed on the website.

    Fields:
        update (OneToOneField): A foreign key relationship with the LatestUpdate model, indicating which update is featured.
        on_delete=models.CASCADE specifies that if a LatestUpdate object is deleted, the corresponding FeaturedNews object will also be deleted.
        created (DateTimeField): The date and time the FeaturedNews object was created, automatically set to the current time using timezone.now().

    Meta options:
        ordering: Orders FeaturedNews objects by their created in descending order, maintaining a consistent order with LatestUpdate objects.
        verbose_name_plural: Sets the plural display name for FeaturedNews objects in the admin interface to 'Featured News'.

    Methods:
        __str__(self): Returns a string representation of the FeaturedNews object, indicating that it's a featured update and including the title of the linked update.
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

    Fields:
        job_title (CharField): The title of the open position, with a maximum length of 200 characters.
        details (TextField): A detailed description of the job responsibilities and requirements.
        posted_don (DateTimeField): The date and time the open position was posted, automatically set to the current time using auto_now_add=True.
        application_link (URLField): A link to the application form or website for applying to the position.

    Methods:
        __str__(self): Returns a string representation of the OpenPosition object, using its job title and posted date.
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


class ExternalMediaContent(models.Model):
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
    Represents a single news or blog press release on the website.

    Fields:
        title (CharField): The title of the press release, with a maximum length of 200 characters.
        image (ImageField): An image associated with  the press release, uploaded to the 'article_images/' folder.
        content (TextField): The detailed content of the press release, formatted as text.
        created (DateTimeField): The date and time the press release was created, automatically set to the current time using timezone.now().
        updated_at (DateTimeField): The date and time the the press was last modified, automatically set to the current time using timezone.now().

    Meta options:
        ordering: Orders LatestUpdate objects by their created in descending order, displaying the most recent updates first.
        verbose_name: Sets the singular display name for LatestUpdate objects in the admin interface to 'Latest Update'.
        verbose_name_plural: Sets the plural display name for LatestUpdate objects in the admin interface to 'Latest Updates'.

    Methods:
        __str__(self): Returns a string representation of the LatestUpdate object, using its title.
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
    

class SocialMediaPost(models.Model):
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


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.name} - {self.email}"


class HeroSection(models.Model):
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


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=100, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
