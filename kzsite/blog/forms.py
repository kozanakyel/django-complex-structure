from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):  # if you use DB, use ModelFrom
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']

class EmailPostForm(forms.Form):   # using no DB
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class SearchForm(forms.Form):
    query = forms.CharField()
    
class AlgoritmicForm(forms.Form):
    input_array = forms.CharField()
