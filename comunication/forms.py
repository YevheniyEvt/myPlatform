from django import forms
from cloudinary.forms import CloudinaryJsFileField
from .models import Articke, Coment

class ArticlesForm(forms.ModelForm):
    
    
    class Meta:
        model = Articke
        fields = ["title", "content", "is_local", "is_global", "is_competition", 'permission', "image"]

        widgets = {
            "image": forms.ClearableFileInput(attrs={
                    "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                    "aria-describedby": "user_avatar_help",
                    "id": "user_avatar",
                    "required": False
            }),
        }


class ComentForm(forms.ModelForm):

    class Meta:
        model = Coment
        fields = ["content"]


class PhotoDirectForm(ArticlesForm):
    image = CloudinaryJsFileField(
        attrs={'class': ""},
        options={
            'tags': "article",
            'crop': 'limit', 'width': 1000, 'height': 1000,
            'eager': [{'crop': 'fill', 'width': 150, 'height': 100}]
        })
    
    
    
