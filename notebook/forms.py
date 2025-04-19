from django import forms

from .models import Topic, Section, Code, Article, Links, Image, Note


class CodeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True
        
    class Meta:
        model = Code
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                "class": "px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 dark:text-white dark:placeholder-gray-400 dark:bg-gray-800",
                'placeholder': "Add a code...",
            })}
        

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].required = True

    class Meta:
        model = Article
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                "class": "px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 dark:text-white dark:placeholder-gray-400 dark:bg-gray-800",
                'placeholder': "Write an article",
            })}


class LinksForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name'
        self.fields['name'].required = True
        self.fields['url'].label = 'Url'
        self.fields['url'].required = True
        self.fields['content'].label = 'Content'
        self.fields['content'].required = False

    class Meta:
        model = Links
        fields = ['name', 'url', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            }),
            "url": forms.URLInput(attrs={
                    "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            }),
            "content": forms.Textarea(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name'
        self.fields['name'].required = True
        self.fields['short_description'].label = 'Description'
        self.fields['short_description'].required = False

    class Meta:
        model = Topic
        fields = ['name', 'short_description']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            }),
            "short_description": forms.Textarea(attrs={
                "class":"block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            })}


class SectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Title'
        self.fields['title'].required = True
        self.fields['description'].label = 'Description'
        self.fields['description'].required = False

    class Meta:
        model = Section
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                "class": "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            }),
            "description": forms.Textarea(attrs={
                "class": "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
            })}

class NotesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required = True

    class Meta:
        model = Note
        fields = ["text"]
        widgets = {
            'text': forms.Textarea(attrs={
                "class": "px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 dark:text-white dark:placeholder-gray-400 dark:bg-gray-800",
                'placeholder': "Write an note",
            })}
