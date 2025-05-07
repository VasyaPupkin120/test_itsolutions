from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, UpdateView
from django.http import HttpRequest, JsonResponse
from django.db.models import Q
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from .models import CashFlow, Category, StatusFlow, Subcategory, TypeFlow, StatusFlow
from .forms import CashFlowForm

def ajax_get_structure_data(request):
    """
    ajax-запрос структуры типов, категорий, подкатегорий, статусов
    """
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
    
    filter_data = JsonResponse(filter_data, encoder=DjangoJSONEncoder, safe=False)
    
    return filter_data



def refrence_data(request):
    return render(request, 'cashflow/refrence_data.html')


class CashflowListView(ListView):
    model = CashFlow
    template_name = "cashflow/listflow.html"

    def get_queryset(self):
        filters = Q()
        if start_date := self.request.GET.get('start_date'):
            filters &= Q(created_at__gte=start_date)
        if end_date := self.request.GET.get('end_date'):
            filters &= Q(created_at__lte=end_date)
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
        return context


def createflow(request: HttpRequest):
    if request.method == 'POST':
        try:
            typeflow_name = request.POST.get('typeflow')
            category_name = request.POST.get('category')
            subcategory_name = request.POST.get('subcategory')
            status_name = request.POST.get('status')
            amount = request.POST.get('amount')
            comment = request.POST.get('comment', '').strip()
            
            if not all([typeflow_name, category_name, subcategory_name, status_name, amount]):
                messages.error(request, "Все обязательные поля должны быть заполнены")
                return redirect('createflow')
            
            typeflow = TypeFlow.objects.get(name=typeflow_name)
            category = Category.objects.get(name=category_name, typeflow=typeflow)
            subcategory = Subcategory.objects.get(name=subcategory_name, supercategory=category)
            status = StatusFlow.objects.get(name=status_name)
            
            cashflow = CashFlow(
                amount=amount,
                comment=comment if comment else "---",
                typeflow=typeflow,
                category=category,
                subcategory=subcategory,
                status=status
            )
            
            cashflow.save()
            
            messages.success(request, "Запись о движении средств успешно создана")
            return redirect('cashflow:cashflowlist')

        except ObjectDoesNotExist as e:
            messages.error(request, f"Ошибка: {str(e)}")
        except ValueError as e:
            messages.error(request, f"Ошибка в данных: {str(e)}")
        except Exception as e:
            messages.error(request, f"Произошла ошибка: {str(e)}")
    return render(request, 'cashflow/createflow.html')


def updateflow(request:HttpRequest, pk):
    print(pk)
    return redirect('cashflow:cashflowlist')


class CashFlowUpdateView(UpdateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/updateflow.html'
    success_url = reverse_lazy('cashflow:cashflowlist')
    context_object_name = 'flow'
    

class CashFlowDeleteView(DeleteView):
    model = CashFlow
    template_name = 'cashflow/confirm_deletecashflow.html'
    success_url = reverse_lazy('cashflow:cashflowlist')
    context_object_name = 'flow'

    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['typeflow'] = self.object.typeflow.name
    #     initial['category'] = self.object.category.name
    #     initial['subcategory'] = self.object.subcategory.name
    #     return initial
