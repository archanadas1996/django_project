from django import forms
from .models import MovieInformationData, CensorInfo, Director, Actor

class CensorInfoForm(forms.ModelForm):
    class Meta:
        model = CensorInfo
        fields = ['rating', 'description']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ['name', 'bio', 'birth_date', 'nationality', 'awards', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'awards': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ['name', 'bio', 'birth_date', 'nationality', 'awards', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'awards': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MovieForm(forms.ModelForm):
    class Meta:
        model = MovieInformationData
        fields = ['title', 'year', 'rating', 'description', 'poster', 
                 'censor_details', 'directed_by', 'actors']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2099'}),
            'rating': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 8.5/10'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'poster': forms.FileInput(attrs={'class': 'form-control'}),
            'censor_details': forms.Select(attrs={'class': 'form-control'}),
            'directed_by': forms.Select(attrs={'class': 'form-control'}),
            'actors': forms.SelectMultiple(attrs={'class': 'form-control', 'size': '5'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the actors field required
        self.fields['actors'].required = True
        # Add help text
        self.fields['actors'].help_text = "Hold Ctrl (Windows) or Command (Mac) to select multiple actors" 