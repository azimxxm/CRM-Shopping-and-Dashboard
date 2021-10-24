from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
