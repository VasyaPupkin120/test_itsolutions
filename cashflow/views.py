from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpRequest, JsonResponse
from django.db.models import Q, Subquery
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import CashFlow, Category, StatusFlow, Subcategory, TypeFlow, StatusFlow
from .forms import CategoryCreateUpdateForm, CreateUpdateCashFlowForm, FilterCashFlowForm, StatusflowCreateUpdateForm, SubcategoryCreateUpdateForm, TypeflowCreateUpdateForm


def ajax_get_structure_data(request):
    """
    ajax-запрос структуры типов, категорий, подкатегорий, статусов
    """
    typeflows = dict(TypeFlow.objects.values_list('pk', "name"))
    categories = dict(Category.objects.values_list('pk', "name"))
    subcategories = dict(Subcategory.objects.values_list('pk', "name"))
    statuses = dict(StatusFlow.objects.values_list('pk', "name"))

    typeflows_and_categories = {}
    for typeflow in TypeFlow.objects.all():
        typeflows_and_categories[typeflow.pk] = [category.pk for category in typeflow.categories.all()]

    categories_and_subcategories = {} 
    for category in Category.objects.all():
        categories_and_subcategories[category.pk] = [subcategory.pk for subcategory in category.subcategories.all()]

    filter_data = {}
    filter_data['typeflows'] = typeflows
    filter_data['categories'] = categories
    filter_data['subcategories'] = subcategories
    filter_data['statuses'] = statuses

    filter_data['typeflows_and_categories'] = typeflows_and_categories
    filter_data['categories_and_subcategories'] = categories_and_subcategories

    filter_data = JsonResponse(filter_data, encoder=DjangoJSONEncoder, safe=False)
    
    return filter_data



class CashflowListView(ListView):
    """
    Список движений.
    """
    model = CashFlow
    template_name = "cashflow/flow_list.html"

    def get_queryset(self):
        filters = Q()
        if start_date := self.request.GET.get('start_date'):
            filters &= Q(created_at__gte=start_date)
        if end_date := self.request.GET.get('end_date'):
            filters &= Q(created_at__lte=end_date)
        if typeflow := self.request.GET.get('typeflow'):
            filters &= Q(typeflow=typeflow)
        if category := self.request.GET.get('category'):
            filters &= Q(category=category)
        if subcategory := self.request.GET.get('subcategory'):
            filters &= Q(subcategory=subcategory)
        if status := self.request.GET.get('status'):
            filters &= Q(status=status)

        return CashFlow.objects.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = FilterCashFlowForm
        return context


class CashFlowCreateView(CreateView):
    model = CashFlow
    form_class = CreateUpdateCashFlowForm
    template_name = 'cashflow/flow_create.html'
    success_url = reverse_lazy('cashflow:flow-list')
    context_object_name = 'flow'


class CashFlowUpdateView(UpdateView):
    model = CashFlow
    form_class = CreateUpdateCashFlowForm
    template_name = 'cashflow/flow_update.html'
    success_url = reverse_lazy('cashflow:flow-list')
    context_object_name = 'flow'


class CashFlowDeleteView(DeleteView):
    model = CashFlow
    template_name = 'cashflow/flow_confirm_delete.html'
    success_url = reverse_lazy('cashflow:flow-list')
    context_object_name = 'flow'


def refrence_data(request):
    typeflows = TypeFlow.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    statuses = StatusFlow.objects.all()
    context = {"typeflows": typeflows,
               "categories": categories,
               "subcategories": subcategories,
               "statuses": statuses,
               }
    return render(request, 'cashflow/refrence_list.html', context)

class RefrenceTypeflowCreateView(CreateView):
    model = TypeFlow
    form_class = TypeflowCreateUpdateForm
    template_name = 'cashflow/refrence_typeflow_create.html'
    success_url = reverse_lazy("cashflow:refrence-list")
    context_object_name = 'typeflow'


class RefrenceCategoryCreateView(CreateView):
    model = Category
    form_class = CategoryCreateUpdateForm
    template_name = 'cashflow/refrence_category_create.html'
    success_url = reverse_lazy("cashflow:refrence-list")
    context_object_name = 'category'


class RefrenceSubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryCreateUpdateForm
    template_name = 'cashflow/refrence_subcategory_create.html'
    success_url = reverse_lazy("cashflow:refrence-list")
    context_object_name = 'subcategory'


class RefrenceStatusflowCreateView(CreateView):
    model = StatusFlow
    form_class = StatusflowCreateUpdateForm
    template_name = 'cashflow/refrence_statusflow_create.html'
    success_url = reverse_lazy("cashflow:refrence-list")
    context_object_name = 'statusflow'
