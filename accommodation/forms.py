from django.forms import ModelForm
from .models import Accommodation

class AccommodationForm(ModelForm):
    class Meta:
        model = Accommodation
        #fields = '__all__'
        exclude = ('user',)
        #exclude = ('date',)
        #widgets = {'estimated_end': DateInput(attrs={'type':'date'}),}
