from django.contrib import admin

from .models import Accommodation,City, Country, Reservation, Payment

# Register your models here.

admin.site.register(Accommodation)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Reservation)
admin.site.register(Payment)
