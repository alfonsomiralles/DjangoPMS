from django import forms
from accommodation.models import Reservation, Country, City
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
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}), required=False)
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}),required=False) 
    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        required=False,
        empty_label="Mostrar Todos"
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=False,
        empty_label="Mostrar Todas"
    )

class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('at_hotel', 'Pay at Hotel')
    ])
    start_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=DateInput(attrs={'type': 'date'}))

  