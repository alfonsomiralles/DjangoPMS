from django.shortcuts import render, redirect
from .models import Accommodation
from .forms import AccommodationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

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
    accommodation = Accommodation.objects.get(id=id)
    if request.method == 'POST':
        form = AccommodationForm(request.POST,instance=accommodation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Alojamiento actualizado')
            return redirect(to='accommodation')
        else:
            messages.error(request, 'El Alojamiento no ha podido ser modificado')
            return redirect(to='accommodation')    
    else:
        form = AccommodationForm(instance=accommodation)
        context = {
            'form':form,
            'id':id
        }
    return render(request, 'accommodations/edit.html', context)

class AccommodationCreate(LoginRequiredMixin,CreateView):
    model = Accommodation
    form = AccommodationForm
    fields = ['name','description','address','email','phone','mobile','image','is_active','country','city','price',]
    success_url = reverse_lazy('accommodation')
    success_message = 'Alojamiento creado con éxito!'
    error_message = 'Se ha producido un error. Alojamiento no creado'

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, self.success_message)
        return super(AccommodationCreate, self).form_valid(form)  

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)      


@login_required
def delete(request, id):
    accommodations = Accommodation.objects.get(id=id)
    accommodations.delete()
    messages.success(request, 'Alojamiento borrado')
    return redirect('accommodation')
