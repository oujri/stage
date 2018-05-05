from django import forms
from .models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('description', 'image', )


class NewslatterForm(forms.Form):
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
