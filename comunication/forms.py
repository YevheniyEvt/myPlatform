from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Articke, Coment



class ArticlesForm(forms.ModelForm):

    PERMISSION_CHOICES = [
        ('all', 'All'),
        ('district', 'District'),
        ('region', 'Region'),
    ]

    class Meta:
        model = Articke
        fields = ["title", 'content', 'permission', 'is_local', 'is_global', 'is_competition', 'image']
    
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(
            attrs={
            "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            "id": "title",
            'placeholder': "Title of article",
        }))
    
    content = forms.CharField(
        label='Content',
        widget=forms.Textarea(
            attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                "id": "content",
                'placeholder': "Your text here",
            }))
    
    permission=forms.ChoiceField(
        label='Permission',
        choices=PERMISSION_CHOICES,
        initial = ['all'],
        widget=forms.Select(
            attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                "id": "permission",
            }))

    is_local=forms.BooleanField(
        label='Local',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
                "id": "is_local",
        }))
    
    is_global=forms.BooleanField(
        label='Global',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
                "id": "is_global",
        }))
    
    is_competition=forms.BooleanField(
        label='Competition',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600",
                "id": "is_competition",
        }))
    
    image=CloudinaryFileField(
        label='Image',
        required=False,
        widget=forms.ClearableFileInput(
        attrs={
            "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
            "aria-describedby": "user_avatar_help",
            "id": "image",
            }),
        options={
            'tags': "article",
            'crop': 'limit', 'width': 1000, 'height': 1000,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 100}]
        })
    

class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ["content"]


    
    
