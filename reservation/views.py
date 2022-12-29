from django.shortcuts import render, redirect, get_object_or_404
from accommodation.models import Accommodation, Reservation, Payment
from django.contrib import messages
from .forms import ReservationForm, PaymentForm
from django.http import HttpResponse
from django.template.loader import render_to_string
import pdfkit
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

@login_required
def accommodations_list(request):
    active_accommodations = Accommodation.objects.filter(is_active=True)
    context = {
        'accommodations': active_accommodations
    }
    return render(request, 'accommodations/list.html', context)   

    
@login_required
def reserve(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            if not accommodation.is_available(start_date, end_date):
                messages.error(request, "Lo sentimos, este alojamiento no está disponible en esas fechas.")
                return redirect("accommodations")
            reservation = form.save(commit=False)
            reservation.accommodation = accommodation
            reservation.user = request.user
            # Recuperamos el precio del alojamiento y calculamos el precio total de la reserva
            price = accommodation.price
            total_price = price * (end_date - start_date).days
            reservation.total_price = total_price
            reservation.save()
            messages.success(request, "Reserva realizada con éxito. Por favor realiza el pago.")
            return redirect("pay", reservation.pk)
    else:
        form = ReservationForm()
    return render(request, "reservations/reserve.html", {"form": form, "accommodation": accommodation})

@login_required
def pay(request, id):
    # View function to display the payment form
    # and handle the payment submission
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']
            if payment_method == 'at_hotel':
                payment_status = 'pending'
            else:
                payment_status = 'paid'
            payment = Payment.objects.create(
                reservation=reservation,
                payment_method=payment_method,
                amount=reservation.total_price,
                status=payment_status
            )
            paymentid = payment.pk
            return redirect(to='invoice', id=paymentid)
    else:
        form = PaymentForm()
    context = {
        'form': form,
        'reservation': reservation
    }
    return render(request, 'reservations/pay.html', context)  

@login_required
def invoice(request, id):
    payment = get_object_or_404(Payment, id=id)
    reservation = payment.reservation
    number_of_nights = (reservation.end_date - reservation.start_date).days
    context = {
        'payment': payment,
        'reservation': reservation,
        'number_of_nights': number_of_nights
    }
    return render(request, 'reservations/invoice.html', context)