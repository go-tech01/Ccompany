from django.forms import ModelForm
from django import forms
from estimateapp.models import EstimateModel


class ImageCreationForm(ModelForm):
    input_estimateimage = forms.FileField(widget=forms.ClearableFileInput(attrs={"style" :"display:none",
                                                                   "name":"inpFile",
                                                                    "id":"inpFile",
                                                                 'multiple':True}))
    class Meta:
        model = EstimateModel
        fields = '__all__'
        phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '010-0000-0000'}))