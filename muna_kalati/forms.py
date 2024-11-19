from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control w-50 rounded-4 me-3', 'placeholder': 'Your Name', 'required': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control w-50 rounded-4', 'placeholder': 'Your Email', 'required': 'true'}),
            'message': forms.Textarea(attrs={'class': 'form-control rounded-4', 'rows': 4, 'placeholder': 'Your Message', 'required': 'true'}),
        }

        
