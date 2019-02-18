# coding = utf-8
# 存放表单代码

from django import forms
from .models import *

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']