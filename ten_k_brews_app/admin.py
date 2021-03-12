from django.contrib import admin
from .models import Establishment, Drink, UserData

# Register your models here.
admin.site.register(Establishment)
admin.site.register(Drink)
admin.site.register(UserData)
