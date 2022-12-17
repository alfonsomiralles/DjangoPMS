from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='accommodations'),
    path('view/<int:id>', views.view, name='acc_view'),
    path('accommodation/', views.accommodation, name='accommodation'),
    path('accommodation/<int:id>', views.accommodation, name='accommodation'),
    path('delete/<int:id>', views.delete, name='acc_delete'),
]
