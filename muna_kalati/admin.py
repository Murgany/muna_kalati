from django.contrib import admin
from .models import UserProfile, LatestUpdate, FeaturedNews, OpenPosition, ExternalMediaContent, PressRelease, Category, SocialMediaPost, Contact, HeroSection, TeamMember
from django.utils.html import format_html
import pytz

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# @admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'created')
    search_fields = ['category_name']
    list_filter = ['created']


class LatestUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author__username', 'created', 'created_in_gmt')
    search_fields = ['title', 'author__username']
    list_filter = ['category', 'author__username']

    def created_in_gmt(self, obj):
        # Convert the created field to GMT
        gmt_timezone = pytz.timezone('GMT')
        return obj.created.astimezone(gmt_timezone).strftime('%Y-%m-%d %H:%M:%S %Z')

    created_in_gmt.short_description = 'Created (GMT)'


class FeaturedNewsAdmin(admin.ModelAdmin):
    # Display specific fields in the admin list view
    list_display = ('get_update_title', 'created')

    # Create a custom method to display the title of the related LatestUpdate model
    def get_update_title(self, obj):
        return obj.update.title
    get_update_title.short_description = 'Update Title'  # Set the column name


class OpenPositionAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'posted_on')
    search_fields = ['job_title', 'posted_on']
    list_filter = ['job_title', 'posted_on']

class ExternalMediaContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'created')
    search_fields = ['title', 'source', 'created']
    list_filter = ['title', 'source', 'created']

class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ['title', 'created']
    list_filter = ['title', 'created']

class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')
    search_fields = ['title', 'created']
    list_filter = ['title', 'created']


class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ('platform', 'created')
    search_fields = ['platform', 'created']
    list_filter = ['platform', 'created']

class ContactAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'date')
    search_fields = ['name', 'date']
    list_filter = ['date', 'date']
    readonly_fields = ('name', 'email', 'message', 'date')  # Set fields as read-only

    def has_add_permission(self, request):
        return False  # Disables adding new Contact entries

    def has_change_permission(self, request, obj=None):
        return False  # Disables editing Contact entries

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'title')
    search_fields = ['name', 'title']
    list_filter = ['name', 'title']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]  
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'get_title', 'display_profile_picture')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
    
    def get_title(self, obj):
        return obj.profile.title
    get_title.short_description = 'Title'
    get_title.admin_order_field = 'profile__title'


    def display_profile_picture(self, obj):
        # Access the related profile object
        if hasattr(obj, 'profile') and obj.profile.profile_picture:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; border-radius: 25px;" />',
                obj.profile.profile_picture.url
            )
        return "No Image"

    display_profile_picture.short_description = 'Profile Picture'


# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'title', 'get_profile_picture')
#     search_fields = ('user__username', 'title')
#     list_filter = ('title',)

#     def get_profile_picture(self, obj):
#         if obj.profile_picture:
#             return format_html(f'<img src="{obj.profile_picture.url}" style="width: 50px; height: 50px;" />')
#         return "No Image"
#     get_profile_picture.short_description = 'Profile Picture'

# admin.site.register(UserProfile, UserProfileAdmin)


# Unregister the default User admin
admin.site.unregister(User)

# Register the customized User admin
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




