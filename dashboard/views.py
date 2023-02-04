from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reservation.models import Reservation
from accommodation.models import Accommodation

# Create your views here.
def index(request):
    return render(request, 'index.html', {})

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