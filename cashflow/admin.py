from django.contrib import admin

from .models import Category, StatusFlow, TypeFlow, CashFlow 

admin.site.register(Category)
admin.site.register(StatusFlow)
admin.site.register(TypeFlow)
admin.site.register(CashFlow)
