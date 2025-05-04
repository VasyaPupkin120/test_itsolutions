from django.contrib import admin
from django import forms

from .models import TypeFlow, Category, Subcategory, StatusFlow, CashFlow 


################################################################################
# классы-инлинеры
################################################################################
class CashFlowInline(admin.TabularInline):
    """
    Отображение связанных записей движений
    """
    model = CashFlow
    fields = ('amount', 'typeflow', 'category', 'subcategory', 'status', 'created_at', 'comment')
    readonly_fields = ('amount', 'typeflow', 'category', 'subcategory', 'status', 'created_at', 'comment')
    extra = 0


class CategoryInline(admin.TabularInline):
    """
    Для отображения связанных категорий
    """
    model = Category
    extra = 1


class SubcategoryInline(admin.TabularInline):
    """
    Для отображения связанных подкатегорий
    """
    model = Subcategory
    extra = 1

################################################################################
# классы-редакторы
################################################################################

class TypeFlowAdmin(admin.ModelAdmin):
    inlines = (CategoryInline,)
    list_display = ['name']


class CategoryAdmin(admin.ModelAdmin):
    inlines = (SubcategoryInline,)
    list_display = ['name', 'typeflow'] 
    

class SubcategoryAdmin(admin.ModelAdmin):
    inlines = (CashFlowInline, )
    list_display = ['name', 'supercategory'] 


class StatusFlowAdmin(admin.ModelAdmin):
    inlines = (CashFlowInline,)
    list_display = ['name']


class CashFlowAdmin(admin.ModelAdmin):
    list_display = ['amount', 'typeflow', 'category', 'subcategory', 'status', 'created_at', 'comment']
    widgets = {
        'comment': forms.Textarea(attrs={'rows': 2, 'cols': 20}),
    }

################################################################################
# регистрация
################################################################################

admin.site.register(TypeFlow, TypeFlowAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(StatusFlow, StatusFlowAdmin)
admin.site.register(CashFlow, CashFlowAdmin)
