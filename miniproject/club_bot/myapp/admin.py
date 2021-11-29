from django.contrib import admin

from .models import *

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Gym)
admin.site.register(occasion)
admin.site.register(Order_occasion)
admin.site.register(OrderItem_occasion)
# Register your models here.
