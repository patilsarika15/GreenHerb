from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Select an image')


class PlantSearchForm(forms.Form):
    plant_name = forms.CharField(label='Plant Name', max_length=100)
