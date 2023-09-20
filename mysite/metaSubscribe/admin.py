from django.contrib import admin
from .models import Dataset, CustomUser

admin.site.register(Dataset)
admin.site.register(CustomUser)

# Register your models here.
