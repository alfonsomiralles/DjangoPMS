from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='reservation'),
    path('accommodationssearch/', views.search, name='accommodationssearch'),
    path('accommodationslist/', views.search_results, name='accommodationslist'),
    path('accommodations/<int:pk>/reserve/', views.reserve, name='reserve'),
    path('invoice/<int:id>/', views.invoice, name='invoice'),
    path('reservations/', views.reservations, name='reservations'),
    path('reservations_view/<int:id>/', views.reservations_view, name='reservations_view'),
    path('reservations_delete/<int:id>', views.reservations_delete, name='reservations_delete'),
    path('reservations_list/', views.reservations_list, name='reservations_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('reserve_search/', views.reserve_search, name='reserve_search'),
    path('leave_review/<int:id>/', views.leave_review, name='leave_review'),
    path('review_list/<int:id>/', views.review_list, name='review_list'),
]