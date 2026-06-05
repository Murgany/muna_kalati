"""
Django Forms for Muna Kalati Application

This module contains form classes for user input validation and processing.

Forms:
    - ContactForm: Handles contact form submissions from website visitors
"""

from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Contact form for capturing visitor inquiries.
    
    This ModelForm is based on the Contact model and provides
    a user-friendly interface for submitting contact messages.
    
    Model:
        Contact: Stores contact form submissions
    
    Fields Included:
        - name (CharField): Visitor's full name
        - email (EmailField): Visitor's email address
        - message (TextField): Message content
    
    Field Validation:
        - name: Required, max 100 characters
        - email: Required, must be valid email format
        - message: Required, textarea input
    
    Widgets Customization:
        - Bootstrap styling: Uses Bootstrap form-control class
        - Rounded inputs: rounded-4 class for rounded corners
        - Responsive layout: Uses Bootstrap width utilities
        - Custom placeholders: User-friendly placeholder text
        - Required attributes: HTML5 required attribute
    
    Rendering:
        Each field uses custom HTML attributes for styling and UX:
        
        name field:
        - Type: TextInput (single-line text)
        - Classes: form-control w-50 rounded-4 me-3
        - Placeholder: "Your Name"
        - HTML5 required: true
        
        email field:
        - Type: EmailInput (email validation)
        - Classes: form-control w-50 rounded-4
        - Placeholder: "Your Email"
        - HTML5 required: true
        
        message field:
        - Type: Textarea (multi-line text)
        - Classes: form-control rounded-4
        - Rows: 4 lines visible
        - Placeholder: "Your Message"
        - HTML5 required: true
    
    CSS Classes Explained:
        - form-control: Bootstrap styling for form inputs
        - w-50: Width 50% (width utility)
        - rounded-4: Bootstrap rounded corners (level 4)
        - me-3: Margin-end (right) spacing
    
    Usage in Views:
        >>> from .forms import ContactForm
        >>> if request.method == 'POST':
        ...     form = ContactForm(request.POST)
        ...     if form.is_valid():
        ...         form.save()
        ...         # Handle success
    
    Usage in Templates:
        {% csrf_token %}
        <form method="post">
            {{ form.name }}
            {{ form.email }}
            {{ form.message }}
            <button type="submit">Send</button>
        </form>
    
    Form Validation Flow:
        1. User submits form with POST data
        2. Form validates required fields
        3. Email validation happens automatically
        4. If valid, Contact object is created in database
        5. Success message is displayed to user
    
    Data Persistence:
        - Submissions are saved to Contact model
        - Admins can view/manage in Django admin
        - Contact admin prevents editing (read-only)
    
    Accessibility:
        - All fields marked as required (HTML5)
        - Clear placeholder text
        - Proper form structure
    
    Browser Validation:
        - HTML5 email validation
        - Required field validation
        - Form submission prevents on invalid data
    
    Server-Side Validation:
        - Django form validation layer
        - Model validation (Contact model)
        - Additional checks possible via clean() methods
    
    Meta Options:
        model: Contact (the model this form is based on)
        fields: List of fields to include in form
        widgets: Custom widget definitions for each field
    
    Notes:
        - Form doesn't include 'date' field (auto-set in model)
        - Bootstrap 4/5 compatible
        - Consider adding CAPTCHA for spam prevention
        - Email notifications could be added on save
    """
    
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control w-50 rounded-4 me-3',
                'placeholder': 'Your Name',
                'required': 'true'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control w-50 rounded-4',
                'placeholder': 'Your Email',
                'required': 'true'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control rounded-4',
                'rows': 4,
                'placeholder': 'Your Message',
                'required': 'true'
            }),
        }

    def clean_email(self):
        """
        Validate email field format and existence.
        
        Returns:
            str: Cleaned and validated email address
        
        Raises:
            ValidationError: If email format is invalid
        
        Custom Validation Logic:
            This method is called during form validation
            after Django's built-in email validation.
            
            Could add additional checks like:
            - Blacklist certain domains
            - Check against existing contacts
            - Rate limiting per email
        """
        email = self.cleaned_data.get('email')
        return email

    def clean_name(self):
        """
        Validate name field content.
        
        Returns:
            str: Cleaned name
        
        Custom Validation Logic:
            This method is called during form validation.
            
            Could add checks like:
            - Minimum length requirement
            - Character type validation
            - Profanity filtering
        """
        name = self.cleaned_data.get('name')
        return name

    def clean_message(self):
        """
        Validate message field content.
        
        Returns:
            str: Cleaned message
        
        Custom Validation Logic:
            This method is called during form validation.
            
            Could add checks like:
            - Minimum message length
            - Maximum message length
            - Profanity filtering
            - Spam detection
        """
        message = self.cleaned_data.get('message')
        return message
