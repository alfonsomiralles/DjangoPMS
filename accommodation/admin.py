from django.contrib import admin

from .models import Accommodation,City, Country, Image

# Register your models here.

class AccommodationAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'city', 'is_active', 'default_price', 'user']   

class ImageAdmin(admin.ModelAdmin):
    list_display = ('accommodation', 'image')      

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'postcode','country')       

class CountryAdmin(admin.ModelAdmin):
    list_display = ('country_name', 'country_code')  

admin.site.register(Accommodation, AccommodationAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(Image, ImageAdmin)


