from django import forms
from .models import Item, Profile, Message

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'category', 'image', 'description', 'location', 'expiry_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 5 Extra Mangoes'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the item...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Koramangala, Bengaluru'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell your neighbors a bit about yourself...'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Type your private message...', 'class': 'form-control rounded-pill px-4 py-2'}),
        }
        labels = {'text': ''}