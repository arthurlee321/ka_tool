from django.contrib import admin
from .models import Customer, SKU, Pricing, Promotion, Result

# Register your models here.
admin.site.register(Customer)
admin.site.register(SKU)
admin.site.register(Pricing)
admin.site.register(Promotion)
admin.site.register(Result)