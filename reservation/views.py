from django.shortcuts import render, redirect, get_object_or_404
from accommodation.models import Accommodation, Reservation, Payment, Price, Review
from django.contrib import messages
from .forms import PaymentForm, SearchForm, ReviewForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import date
from django.db.models import Avg


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
            start_date = form.cleaned_data["fecha_inicio"]
            end_date = form.cleaned_data["fecha_fin"]
            country = form.cleaned_data["pais"]
            city = form.cleaned_data["ciudad"]
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
def reserve_search(request):
    active_accommodations = Accommodation.objects.filter(
        name__contains=request.GET.get('search', ''))
    context = {
        'accommodations': active_accommodations,
    }
    return render(request, 'accommodations/list.html', context)    

@login_required
def accommodations_list(request):
    active_accommodations = Accommodation.objects.filter(is_active=True).annotate(average_rating=Avg('review__rating'))
    context = {
        'accommodations': active_accommodations
    }
    return render(request, 'accommodations/list.html', context)



def process_payment(payment_method):
    if payment_method == "en_hotel":
        # Si el pago se realizará en el hotel, no hace falta procesar el pago
        return "Pendiente"
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
            payment_method = form.cleaned_data["metodo_de_pago"]
            # Procesar el pago utilizando la función process_payment
            status = process_payment(payment_method)
            start_date = form.cleaned_data["fecha_inicio"]
            end_date = form.cleaned_data["fecha_fin"]
            if not accommodation.is_available(start_date, end_date):
                messages.error(request, "Lo sentimos, este alojamiento no está disponible en esas fechas.")
                return redirect("accommodations")
            # Utilizar el método get_price para obtener el precio correcto
            price = accommodation.default_price
            total_price = price * (end_date - start_date).days    
            # Crear una instancia del modelo Reservation
            reservation = Reservation(
                start_date=start_date,
                end_date=end_date,
                accommodation=accommodation,
                user=request.user,
                total_price=total_price,
            )
            reservation.save()
            # Crear una instancia del modelo Payment
            payment = Payment(
                reservation=reservation,
                payment_method=payment_method,
                amount=total_price,
                status=status
            )
            payment.save()
            messages.success(request, "Reserva realizada con éxito.")
            return redirect("reservations")
    else:
        form = PaymentForm()
    return render(request, "reservations/reserve.html", {"form": form, "payment_form": payment_form, "accommodation": accommodation,})


@login_required
def invoice(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    payment = Payment.objects.get(reservation=reservation)
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
def leave_review(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    # Comprobar que la fecha de hoy es superior a la fecha de salida antes de permitir la publicación de una reseña
    if date.today() <= reservation.end_date:
        messages.error(request, 'Solo puedes publicar una reseña cuando se complete la estancia')
        return redirect('reservations')
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Guardar la reseña en la base de datos y asociarla con la reserva correspondiente
            review = form.save(commit=False)
            review.reservation = reservation
            review.user = request.user
            review.accommodation = reservation.accommodation #Aquí estableces la relación con la columna "accommodation_id"
            review.save()
            messages.success(request, 'Reseña publicada')
            return redirect('reservations')
    else:
        form = ReviewForm()
    context = {
        'form': form,
        'reservation': reservation,
    }
    return render(request, 'reservations/leave_review.html', context) 

@login_required  
def review_list(request,id):
    accommodation = get_object_or_404(Accommodation, id=id)
    reviews = Review.objects.filter(accommodation=accommodation)
    if not reviews:
        message = "No hay reseñas publicadas todavía."
    else:
        message = ""
    context = {
        'reviews': reviews, 
        'message': message,
        'accommodation':accommodation}
    return render(request, 'reservations/review_list.html', context)

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

@login_required
def dashboard(request):
    # Numero de reservas
    reservations = Reservation.objects.filter(accommodation__user=request.user).count()
    # Numero de alojamientos creados
    accommodations = Accommodation.objects.filter(user=request.user).count()
    # Numero de reservas realizadas por el usuario
    user_reservations = Reservation.objects.filter(user=request.user).count()

    context = {
        'reservations': reservations,
        'accommodations': accommodations,
        'user_reservations': user_reservations,
    }
    return render(request, 'reservations/dashboard.html', context)
