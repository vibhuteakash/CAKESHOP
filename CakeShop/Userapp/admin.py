from django.contrib import admin
from .models import Payments

# Register your models here.

class PaymentsAdmin(admin.ModelAdmin):
    list_display=('card_no','expiry','cvv','balance')



admin.site.register(Payments,PaymentsAdmin)
