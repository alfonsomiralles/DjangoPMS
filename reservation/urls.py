from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reservation'),
    path('accommodationslist/', views.accommodations_list, name='accommodationslist'),
    path('accommodations/<int:pk>/reserve/', views.reserve, name='reserve'),
    path('pay/<int:id>/', views.pay, name='pay'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('reservations/', views.reservations, name='reservations'),
    path('reservations_view/<int:id>/', views.reservations_view, name='reservations_view'),
    path('reservations_edit/<int:id>', views.reservations_edit, name='reservations_edit'),
    path('reservations_delete/<int:id>', views.reservations_delete, name='reservations_delete'),
]