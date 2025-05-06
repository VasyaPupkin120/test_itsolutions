from django.shortcuts import render
from django.views.generic import ListView
from django.http import JsonResponse
from django.db.models import Q
import json 

from .models import CashFlow, Category, StatusFlow, Subcategory, TypeFlow


def createflow(request):
    return render(request, 'cashflow/createflow.html')

def refrence_data(request):
    return render(request, 'cashflow/refrence_data.html')


class CashflowList(ListView):
    model = CashFlow
    template_name = "cashflow/listflow.html"

    def get_queryset(self):
        filters = Q()
        if start_datetime := self.request.GET.get('start_datetime'):
            filters &= Q(created_at__gt=start_datetime)
        if end_datetime := self.request.GET.get('end_datetime'):
            filters &= Q(created_at__lt=end_datetime)
        if typeflow := self.request.GET.get('typeflow'):
            filters &= Q(typeflow__name=typeflow)
        if category := self.request.GET.get('category'):
            filters &= Q(category__name=category)
        if subcategory := self.request.GET.get('subcategory'):
            filters &= Q(subcategory__name=subcategory)
        if status := self.request.GET.get('status'):
            filters &= Q(status__name=status)

        return CashFlow.objects.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        typeflows = list(TypeFlow.objects.values_list("name", flat=True))
        categories = list(Category.objects.values_list("name", flat=True))
        subcategories = list(Subcategory.objects.values_list("name", flat=True))
        statuses = list(StatusFlow.objects.values_list("name", flat=True))

        typeflows_and_categories = {}
        for typeflow in TypeFlow.objects.all():
            typeflows_and_categories[typeflow.name] = [category.name for category in typeflow.categories.all()]

        categories_and_subcategories = {} 
        for category in Category.objects.all():
            categories_and_subcategories[category.name] = [subcategory.name for subcategory in category.subcategories.all()]

        filter_data = {}
        filter_data['typeflows'] = typeflows
        filter_data['categories'] = categories
        filter_data['subcategories'] = subcategories
        filter_data['statuses'] = statuses

        filter_data['typeflows_and_categories'] = typeflows_and_categories
        filter_data['categories_and_subcategories'] = categories_and_subcategories
        
        context["filter_data"] = json.dumps(filter_data, ensure_ascii=False)
        
        return context
