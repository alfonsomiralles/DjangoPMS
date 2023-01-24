from django import forms
from accommodation.models import Reservation, Country, City, Review
from django.forms import DateInput

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date',]

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})

class SearchForm(forms.Form):
    fecha_inicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    fecha_fin = forms.DateField(widget=DateInput(attrs={'type': 'date'}),required=False) 
    pais = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Mostrar Todos"
    )
    ciudad = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label="Mostrar Todas"
    )

class PaymentForm(forms.Form):
    metodo_de_pago = forms.ChoiceField(choices=[
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia_bancaria', 'Transferencia Bancaria'),
        ('en_hotel', 'Pago en Hotel')
    ])
    fecha_inicio = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'review']
        labels = {
                'rating': 'calificación',
                'title': 'titulo',
                'review': 'reseña',
                }

    rating = forms.IntegerField(min_value=1, max_value=5)
    title = forms.CharField(max_length=255)
    review = forms.CharField(widget=forms.Textarea)  