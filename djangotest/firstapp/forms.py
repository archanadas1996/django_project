from django import forms
from .models import MovieInformationData

class MovieForm(forms.ModelForm):
    class Meta:
        model = MovieInformationData
        fields = ['title', 'year', 'director', 'rating', 'description', 'poster']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2099'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 8.5/10'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'poster': forms.FileInput(attrs={'class': 'form-control'})
        } 