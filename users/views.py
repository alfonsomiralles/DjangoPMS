from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado con éxito')
            return redirect('index')
        else:
            messages.error(request, 'El Usuario no ha podido ser creado')
            return redirect('register')
    else:
        form = UserCreationForm
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)


def profile(request):
    current_user = request.user
    context = {
        'current_user': current_user
    }
    return render(request,'users/profile.html',context)


def view(request, id):
    profile = User.objects.get(id=id)
    context = {
        'profile': profile
    }
    return render(request,'users/detail.html',context)   


def edit(request, id):
    profile = User.objects.get(id=id)
    if request.method == 'GET':
        form = UserChangeForm(instance = profile)
        context = {
            'form': form,
            'id': id
        }
        return render(request,'users/edit.html',context)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
        messages.success(request, 'Perfil actualizado') 
        context = {
            'form': form,
            'id': id
        } 
        return render(request,'users/edit.html',context)  


def delete(request, id):
    todo = User.objects.get(id=id)
    todo.delete()
    return redirect('index')         