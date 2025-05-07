from django import forms

from cloudinary.forms import CloudinaryFileField

from .models import Topic, Section, Code, Article, Links, Image, Note

class CodeForm(forms.ModelForm):
    class Meta:
        model = Code
        fields = ['content']

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['content']

class LinksForm(forms.ModelForm):
    class Meta:
        model = Links
        fields = ['name', 'content', 'url']

        widgets = {
            'name': forms.TextInput(attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                "required": True,
                "id": "name" 
            }),
            "content": forms.Textarea(attrs={
                "rows": "2",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                "id": "content",
                "required": False

            }),
            "url": forms.URLInput(attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    "required": True,
                    "id": "url" 

            }),
        }



class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image_title'].label = 'Title'
        self.fields['image_title'].required = True
        self.fields['image_description'].label = 'Description'
        self.fields['image_description'].required = False
        self.fields['image_file'].label = 'Image'
        self.fields['image_file'].required = True

    class Meta:
        model = Image
        fields = ['image_title', 'image_description', 'image_file']
        widgets = {
            'image_title': forms.TextInput(attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            }),
            "image_description": forms.Textarea(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",

            }),
            "image_file": forms.ClearableFileInput(attrs={
                    "class": "block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400",
                    "aria-describedby": "user_avatar_help",
  
            })}

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'short_description']


class SectionForm(forms.ModelForm):
    
    class Meta:
        model = Section
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                "required": True
            }),
            "description": forms.Textarea(attrs={
                "rows": "4",
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                'value': ''
            }),

        }

class NotesForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = ["text"]