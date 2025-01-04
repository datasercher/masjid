from django.contrib import admin
from .models import Fund, Deposit, Withdrawal, Person, Bazar

admin.site.register(Fund)
admin.site.register(Deposit)
admin.site.register(Withdrawal)
admin.site.register(Person)
admin.site.register(Bazar)
