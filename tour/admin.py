from django.contrib import admin

from .models import Tour, Category, Info
# Register your models here.
admin.site.register(Category)
admin.site.register(Tour)
admin.site.register(Info)
