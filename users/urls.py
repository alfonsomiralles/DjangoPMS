from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='users'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>', views.profile, name='profile'),
    path('view/<int:id>', views.view, name='profile_view'),
    path('edit/<int:id>', views.delete, name='profile_edit'),
    path('delete/<int:id>', views.delete, name='profile_delete')
]