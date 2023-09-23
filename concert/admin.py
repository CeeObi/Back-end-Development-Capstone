from django.contrib import admin

# Register your models here.
from .models import Concert


# class ConcertAdmin(admin.ModelAdmin):
#     fields = ['concert_name', 'duration', 'city', 'date']

admin.site.register(Concert)
#admin.site.register(Concert,ConcertAdmin)
