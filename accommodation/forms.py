from django.forms import ModelForm, TextInput
from .models import Accommodation, Price, Image
from django import forms


class AccommodationForm(ModelForm):

    class Meta:
        model = Accommodation
        fields = '__all__'
        labels = {
                'name': 'Nombre',
                'description': 'Descripción',
                'address': 'Dirección',
                'email': 'Correo electrónico',
                'phone': 'Teléfono',
                'mobile': 'Móvil',
                'image': 'Imagen',
                'is_active': 'Activo',
                'default_price': 'Precio noche por defecto',
                'country': 'País',
                'city': 'Ciudad',
                'user': 'Usuario'
                }
        exclude = ['user']
        widgets = {
            'user': TextInput(attrs={'readonly': 'readonly'})
        }
        #exclude = ('date',)
        #widgets = {'estimated_end': DateInput(attrs={'type':'date'}),}
            

class PriceForm(ModelForm):
    class Meta:
        model = Price
        fields = ['start_date', 'end_date', 'price']
        labels = {
                'start_date': 'fecha_entrada',
                'end_date': 'fecha_salida',
                'price': 'Precio',
                }

    def __init__(self, *args, **kwargs):
        super(PriceForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})    

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',) 
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }      