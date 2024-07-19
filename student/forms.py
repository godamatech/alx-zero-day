from . import models
from django.forms import ModelForm


class RecordForm(ModelForm):

    class Meta:
        model = models.Record
        fields = ["user","title", "description", "file_upload"]
