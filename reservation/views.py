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
                reservations = Reservation.objects.filter(
                    start_date__lte=end_date, end_date__gte=start_date)
                accommodations = accommodations.filter(
                    reservation__in=reservations)
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



def process_payment(payment_method, payment_details):
    if payment_method == "at_hotel":
        # Si el pago se realizará en el hotel, no hace falta procesar el pago
        return "Pago Pendiente"
    else:
        # Si el pago se realizará con otro método, asumir que el pago ha sido exitoso
        return "Pagado"


@login_required
def reserve(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    payment_form = PaymentForm()
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data["payment_method"]
            payment_details = form.cleaned_data["payment_details"]
            # Procesar el pago utilizando la función process_payment
            status = process_payment(payment_method, payment_details)
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            if not accommodation.is_available(start_date, end_date):
                messages.error(request, "Lo sentimos, este alojamiento no está disponible en esas fechas.")
                return redirect("accommodations")
            # Recuperamos el precio del alojamiento y calculamos el precio total de la reserva
            price = accommodation.price
            total_price = price * (end_date - start_date).days    
            # Crear una instancia del modelo Reservation
            reservation = Reservation(
                start_date=start_date,
                end_date=end_date,
                accommodation=accommodation,
                user=request.user,
                # Recuperamos el precio del alojamiento y calculamos el precio total de la reserva
                total_price=total_price,
                # Guardar el status de la reserva según el resultado del procesamiento del pago
                status=status
            )
            reservation.save()
            messages.success(request, "Reserva realizada con éxito.")
            return redirect("reservations")
    else:
        form = PaymentForm()
    return render(request, "reservations/reserve.html", {"form": form, "payment_form": payment_form, "accommodation": accommodation})


@login_required
def invoice(request, id):
    payment = get_object_or_404(Payment, id=id)
    reservation = payment.reservation
    number_of_nights = (reservation.end_date - reservation.start_date).days
    net_total_price = (reservation.total_price / Decimal(1.21))
    iva = reservation.total_price - net_total_price
    context = {
        'payment': payment,
        'reservation': reservation,
        'number_of_nights': number_of_nights,
        'net_total_price': net_total_price,
        'iva': iva,
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
def reservations_delete(request, id):
    reservations = Reservation.objects.get(id=id)
    reservations.delete()
    messages.success(request, 'Reserva cancelada')
    return redirect('reservations')


@login_required
def reservations_list(request):
    # Obtener los alojamientos del usuario actual
    accommodations = Accommodation.objects.filter(user=request.user)

    # Si el usuario tiene alojamientos, obtener las reservas de esos alojamientos
    if accommodations:
        reservations = Reservation.objects.filter(accommodation__in=accommodations)
    else:
        reservations = None

    return render(request, 'reservations/reservations_list.html', {
        'accommodations': accommodations,
        'reservations': reservations,
    })