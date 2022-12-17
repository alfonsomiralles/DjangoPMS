from django.forms import ModelForm, TextInput
from .models import Accommodation

class AccommodationForm(ModelForm):
    class Meta:
        model = Accommodation
        fields = '__all__'
        widgets = {
            'user': TextInput(attrs={'readonly': 'readonly'})
        }
        #exclude = ('date',)
        #widgets = {'estimated_end': DateInput(attrs={'type':'date'}),}
