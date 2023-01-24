from django.urls import path
from . import views
from .views import AccommodationCreate

urlpatterns = [
    path('', views.index, name='accommodations'),
    path('view/<int:id>', views.view, name='acc_view'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('accommodation/<int:id>', views.accommodation, name='accommodation'),
    path('edit/<int:id>', views.edit, name='acc_edit'),
    path('create/', AccommodationCreate.as_view(template_name='accommodations/create.html'), name='acc_create'),
    path('delete/<int:id>', views.delete, name='acc_delete'),
    path('price_edit/<int:id>', views.price_edit, name='price_edit'),
]
