"""
Django Signals for Muna Kalati Application

This module implements Django signal handlers for automated actions
triggered by model events.

Signals:
    - post_save: Triggered after model instances are saved
    
Signal Handlers:
    - create_or_update_user_profile: Automatically create/update UserProfile for new users

Purpose:
    Signals enable decoupled, event-driven logic that responds to
    model lifecycle events without requiring direct code coupling.

Key Concepts:
    - Sender: The model class that triggers the signal (User)
    - Receiver: The function that handles the signal
    - Post-save: Signal sent after model.save() completes
    - Created flag: Indicates whether this is a new instance

Performance Note:
    Signals add overhead to database operations. Use carefully and
    avoid complex logic. Consider management commands for bulk operations.
"""

from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create or update UserProfile for User instances.
    
    This signal handler is triggered after a User is saved in the database.
    It ensures that every User has a corresponding UserProfile object.
    
    Signal Details:
        Sender: User model (django.contrib.auth.models.User)
        Signal Type: post_save
        When Triggered: After User.save() completes successfully
    
    Parameters:
        sender (Model): The model class that sent the signal (User)
        instance (User): The User instance being saved
        created (bool): True if this is a new User, False if updating existing
        **kwargs: Additional signal data (not used here)
    
    Behavior:
        - On User Creation (created=True):
            1. Detect that this is a new user
            2. Create a new UserProfile for the user
            3. Link the UserProfile to the User via one-to-one field
        
        - On User Update (created=False):
            1. Ensure user.profile exists
            2. Save the profile (updates existing profile)
    
    Implementation Logic:
        >>> if created:
        ...     UserProfile.objects.create(user=instance)
        >>> instance.profile.save()
    
    Use Cases:
        1. Auto-provision user profiles:
            - When admin creates new user in admin interface
            - When user registers via custom registration form
            - When user is created programmatically
        
        2. Maintain profile integrity:
            - Ensure every User has a Profile (database constraint)
            - Prevent missing profile errors
            - Enable user.profile access without checks
    
        3. Initialize default values:
            - Profile created with default settings
            - Admin can customize after creation
            - No manual profile creation needed
    
    Related Model:
        UserProfile: One-to-One relationship with User
            Fields:
                - user: OneToOneField(User, on_delete=CASCADE)
                - title: CharField (professional title)
                - profile_picture: ImageField (profile photo)
                - linkedin_url: URLField (LinkedIn profile)
    
    Example Flow:
        1. Admin creates new User in Django admin
        2. User.save() is called
        3. Django sends post_save signal
        4. create_or_update_user_profile() is triggered
        5. UserProfile is automatically created for new user
        6. User now has user.profile accessible
        7. Admin can edit profile inline
    
    Error Handling:
        - IntegrityError: If profile already exists (should not happen)
        - RelatedObjectDoesNotExist: If accessing non-existent profile
        - Protected by database schema (one-to-one constraint)
    
    Performance Considerations:
        - Signal adds ~1-2 database queries per user save
        - Acceptable for typical user creation frequency
        - Problematic for bulk user creation (consider batch_size)
        - For large imports, disable signal or use management command
    
    Troubleshooting:
        
        Issue: "RelatedObjectDoesNotExist: User has no userprofile"
        Cause: Signal didn't run or UserProfile was deleted
        Solution: 
            1. Check signal is properly connected
            2. Manually create missing profiles
            3. Check for signal exceptions in logs
        
        Issue: Duplicate UserProfile creation
        Cause: Signal fired multiple times
        Solution:
            1. Check for multiple signal receivers
            2. Verify instance.profile.save() is idempotent
            3. Review app initialization order
    
    Advanced Topics:
        
        Bulk Operations:
        - QuerySet.update() does NOT trigger signals
        - Use QuerySet.iterator() for memory-efficient signal triggering
        - Consider management commands for bulk user creation
        
        Transaction Handling:
        - Signals fire within same transaction as save
        - Rollback of save also rolls back signal effects
        - Use on_commit hooks for post-transaction actions
        
        Multiple Receivers:
        - Multiple signals can be connected to same sender
        - Order of execution is not guaranteed
        - Use dispatch_uid to prevent duplicate receivers
    
    Testing:
        >>> from django.test import TestCase
        >>> from django.contrib.auth.models import User
        >>> 
        >>> class UserProfileSignalTest(TestCase):
        ...     def test_profile_created_with_user(self):
        ...         user = User.objects.create_user(
        ...             username='testuser',
        ...             email='test@example.com',
        ...             password='testpass123'
        ...         )
        ...         self.assertTrue(hasattr(user, 'profile'))
        ...         self.assertIsNotNone(user.profile)
        ...     
        ...     def test_profile_persists_on_user_update(self):
        ...         user = User.objects.create_user(username='testuser')
        ...         original_profile = user.profile
        ...         
        ...         user.email = 'newemail@example.com'
        ...         user.save()
        ...         
        ...         user.refresh_from_db()
        ...         self.assertEqual(user.profile.id, original_profile.id)
    
    Best Practices:
        1. Keep signal logic simple and focused
        2. Use descriptive function names
        3. Add docstrings explaining the signal
        4. Test signal handlers separately
        5. Monitor signal performance in production
        6. Use signals sparingly (not for every model)
        7. Consider management commands for bulk operations
        8. Document signal dependencies
        9. Use receiver decorator with sender argument
        10. Avoid circular signal dependencies
    
    Django Documentation:
        https://docs.djangoproject.com/en/stable/topics/signals/
        https://docs.djangoproject.com/en/stable/ref/signals/#django.db.models.signals.post_save
    
    Notes:
        - This signal is essential for the CustomUserAdmin inline editing
        - Without this signal, UserProfile would need manual creation
        - The signal makes user management seamless for admins
        - Consider adding pre_save signal for validation if needed
        - Consider adding pre_delete signal for cleanup if needed
    """
    
    # Create a new UserProfile if this is a newly created User
    if created:
        # Create a new UserProfile linked to this user
        UserProfile.objects.create(user=instance)
    
    # Save the user's profile (whether new or existing)
    # This is called on both creation and updates to ensure consistency
    instance.profile.save()
