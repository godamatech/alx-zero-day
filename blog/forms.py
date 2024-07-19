from . import models
from django.forms import ModelForm


class BlogForm(ModelForm):

    class Meta:
        model = models.Blog
        fields = ["title", "body", "level", "lecturer"]
