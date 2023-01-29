from django.contrib import admin

from .models import Accommodation,City, Country, Reservation, Payment, Review, Image

# Register your models here.

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'is_active', 'default_price']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'user', 'start_date', 'end_date', 'total_price')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'payment_method', 'amount')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'user', 'rating', 'review', 'date_created')    

class ImageAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'image')       

admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Image, ImageAdmin)

