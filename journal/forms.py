from django import forms
from .models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('description', 'image', )


class NewsletterForm(forms.Form):
    email = forms.EmailField(
        max_length=40,
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': 'Email:*'}
        ))


class ReplyForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Nom complet:*'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'input',
                'placeholder': 'Email:*'
            }
        )
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'input',
                'placeholder': 'Commentaire:*'
            }
        )
    )


class SignalForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Email:* '
            }
        )
    )
    motif = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Motif:* (max 255)'
            }
        )
    )


class JournalistProfileForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Username'
            }
        )
    )
    telephone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Telephone'
            }
        )
    )
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Prénom'
            }
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Nom'
            }
        )
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Website'
            }
        )
    )
    facebook = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Facebook'
            }
        )
    )
    twitter = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Twitter'
            }
        )
    )
    youtube = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Youtube'
            }
        )
    )
    instagram = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Instagram'
            }
        )
    )
    google_plus = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'Google+'
            }
        )
    )
    linkedin = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                'class': 'form-control border-input',
                'placeholder': 'LinkedIn'
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows': '4',
                'class': 'form-control border-input',
                'placeholder': 'Ici vous pouvez écrire votre description'
            }
        )
    )
