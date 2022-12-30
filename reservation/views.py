from django.shortcuts import render, redirect, get_object_or_404
from accommodation.models import Accommodation, Reservation, Payment
from django.contrib import messages
from .forms import ReservationForm, PaymentForm, SearchForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal

# Create your views here.

def index(request):
    return render(request, 'index.html', {})

@login_required
def search(request):
    form = SearchForm()
    return render(request, 'reservations/partials/searchdate.html', {'form': form})    

@login_required
def search_results(request):
    # Mostrar todos los alojamientos al principio
    accommodations = Accommodation.objects.filter(is_active=True)
    start_date = None
    end_date = None
    country = None
    city = None
    # Si se ha enviado el formulario, procesar la búsqueda
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            country = form.cleaned_data["country"]
            city = form.cleaned_data["city"]
            # Filtrar los alojamientos disponibles en el rango de fechas especificado
            if start_date and end_date:
                reservations = Reservation.objects.filter(start_date__lte=end_date, end_date__gte=start_date)
                accommodations = accommodations.filter(reservation__in=reservations)
            if country:
                accommodations = accommodations.filter(country=country)
            if city:
                accommodations = accommodations.filter(city=city)
    # Enviar los alojamientos filtrados a la plantilla
    context = {
        'accommodations': accommodations,
        'start_date': start_date,
        'end_date': end_date
    }
    return render(request, 'accommodations/list.html', context)

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
                amount=reservation.accommodation.price,
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
    net_total_price = (reservation.total_price / Decimal(1.21))
    context = {
        'payment': payment,
        'reservation': reservation,
        'number_of_nights': number_of_nights,
        'net_total_price': net_total_price,
    }
    return render(request, 'reservations/invoice.html', context)

@login_required
def reservations(request):
    current_user = request.user
    reservations = Reservation.objects.filter(
        id__contains=request.GET.get('search', ''))
    context = {
        'current_user': current_user,
        'reservations': reservations
    }
    return render(request, 'reservations/reservations.html', context)  

@login_required
def reservations_view(request, id):
    reservations = Reservation.objects.get(id=id)
    number_of_nights = (reservations.end_date - reservations.start_date).days
    context = {
        'reservations': reservations,
        'number_of_nights': number_of_nights,
    }
    return render(request, 'reservations/detail.html', context)  

@login_required
def reservations_edit(request, id):
    # Get the reservation object
    reservation = get_object_or_404(Reservation, pk=id)

    if request.method == 'POST':
        # Bind the form to the POST data
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            # Save the updated reservation
            form.save()
            messages.success(request, 'Reserva actualizada')
            return redirect(to='reservations')
        else:
            messages.error(request, 'La reserva no ha podido ser modificada')
            return redirect(to='reservations')    
    else:
        # Display the form for editing the reservation
        form = ReservationForm(instance=reservation)
        context = {
            'form': form,
            'id': id
        }
    return render(request, 'reservations/edit.html', context)    


@login_required
def reservations_delete(request, id):
    reservations = Reservation.objects.get(id=id)
    reservations.delete()
    messages.success(request, 'Reserva cancelada')
    return redirect('reservations')      