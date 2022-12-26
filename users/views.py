from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy
from .forms import MySetPasswordForm
from django.core.mail import send_mail
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado con éxito')
            return redirect('login')
        else:
            messages.error(request, 'El Usuario no ha podido ser creado')
            return redirect('register')
    else:
        form = UserCreationForm
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

@login_required
def profile(request):
    current_user = request.user
    context = {
        'current_user': current_user
    }
    return render(request,'users/profile.html',context)

@login_required
def view(request, id):
    profile = User.objects.get(id=id)
    context = {
        'profile': profile
    }
    return render(request,'users/detail.html',context)   

@login_required
def edit(request,id):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Perfil actualizado')
            return redirect(to='profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'users/edit.html', {'user_form': user_form})
   

@login_required
def delete(request, id):
    todo = User.objects.get(id=id)
    todo.delete()
    messages.success(request, 'Perfil eliminado')
    return redirect('index')         

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = MySetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Contraseña actualizada con éxito")
            return redirect('index')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = MySetPasswordForm(user)
    return render(request, 'users/password_change.html', {'form': form})  

def password_reset(request):
    return render(request, 'password_reset_form.html')  