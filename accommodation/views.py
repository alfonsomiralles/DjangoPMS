from django.shortcuts import render, redirect, get_object_or_404
from .models import Accommodation, Price, Image
from .forms import AccommodationForm, PriceForm, ImageForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_safe

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

@login_required
@require_safe
def price_edit(request, id):
    accommodation = get_object_or_404(Accommodation, id=id)
    prices = Price.objects.filter(accommodation=accommodation)
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            price = form.cleaned_data['price']
            # Verifica si ya existe un precio para esas fechas
            existing_price = Price.objects.filter(accommodation=accommodation, start_date=start_date, end_date=end_date).first()
            if existing_price:
                existing_price.price = price
                existing_price.save()
            else:
                new_price = Price(accommodation=accommodation, start_date=start_date, end_date=end_date, price=price)
                new_price.save()
            messages.success(request, 'Precio actualizado')
            return redirect('accommodation')
    else:
        form = PriceForm()
    return render(request, 'accommodations/price_edit.html', {'form': form, 'prices': prices, 'accommodation': accommodation})   

class AccommodationCreate(LoginRequiredMixin,CreateView):
    model = Accommodation
    form = AccommodationForm
    form_class = AccommodationForm
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

@login_required
def upload_images(request, id):
    accommodation = Accommodation.objects.get(id=id)
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.accommodation = accommodation
            image.save()
            messages.success(request, 'Imagen añadida')
            return redirect(to='accommodation')
        else:
            messages.error(request, 'La imagen no ha podido ser añadida')
            return redirect(to='accommodation')
    else:
        form = ImageForm()
    context = {
        'form':form,
        'id':id
    }
    return render(request, 'accommodations/upload_images.html', context)    

def view_images(request, id):
    accommodation = Accommodation.objects.get(id=id)
    images = Image.objects.filter(accommodation=accommodation)
    context = {
        'accommodation': accommodation,
        'images': images
    }
    return render(request, 'accommodations/view_images.html', context)

