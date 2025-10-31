from django import forms
from .models import Post
from tinymce.widgets import TinyMCE


class postForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','description','featured_image','is_draft']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'id': 'id_title'}),
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            "featured_image" :forms.FileInput(attrs={'accept': 'image/*'}),
            "is_draft" :forms.CheckboxInput()
        }