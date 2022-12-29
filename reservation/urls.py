from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reservation'),
    path('accommodationslist/', views.accommodations_list, name='accommodationslist'),
    path('accommodations/<int:pk>/reserve/', views.reserve, name='reserve'),
    path('pay/<int:id>/', views.pay, name='pay'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
]