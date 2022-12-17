from django.shortcuts import render, redirect
from .models import Accommodation
from .forms import AccommodationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


def index(request):
    return render(request, 'index.html', {})


@login_required
def accommodation(request):
    current_user = request.user
    accommodations = Accommodation.objects.filter(
        name__contains=request.GET.get('search', ''))
    context = {
        'current_user': current_user,
        'accommodations': accommodations
    }
    return render(request, 'accommodations/index.html', context)


@login_required
def view(request, id):
    accommodations = Accommodation.objects.get(id=id)
    context = {
        'accommodations': accommodations
    }
    return render(request, 'accommodations/detail.html', context)


@login_required
def edit(request, id):
    if request.method == 'POST':
        acc_form = AccommodationForm(request.POST, instance=request.user)

        if acc_form.is_valid():
            acc_form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect(to='profile')
    else:
        acc_form = AccommodationForm(instance=request.user)

    return render(request, 'accommodations/edit.html', {'acc_form': acc_form})


@login_required
def delete(request, id):
    accommodations = Accommodation.objects.get(id=id)
    accommodations.delete()
    return redirect('accommodations')