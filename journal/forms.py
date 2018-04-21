from django import forms

from .models import Image


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('description', 'image', )


class NewslatterForm(forms.Form):
    email = forms.EmailField(max_length=40,
                             widget=forms.EmailInput(
                                attrs={
                                    'class': 'input',
                                    'placeholder': 'Enter Your Email'}
                                ))

