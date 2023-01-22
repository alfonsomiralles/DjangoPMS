from django.forms import ModelForm, TextInput
from .models import Accommodation
from django.contrib.auth.models import User

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
                'price': 'Precio por noche',
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
            

        