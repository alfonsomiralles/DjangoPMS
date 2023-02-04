from django.contrib import admin
from .models import Reservation, Payment, Review
# Register your models here.

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'user', 'start_date', 'end_date', 'total_price')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'payment_method', 'amount')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'user', 'rating', 'review', 'date_created') 

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Review, ReviewAdmin)