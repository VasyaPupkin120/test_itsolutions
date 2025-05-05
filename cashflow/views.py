from django.shortcuts import render
from django.views.generic import ListView

from .models import CashFlow

def listflow(request):
    return render(request, 'cashflow/listflow.html')

def createflow(request):
    return render(request, 'cashflow/createflow.html')

def refrence_data(request):
    return render(request, 'cashflow/refrence_data.html')


class CashflowList(ListView):
    model = CashFlow
    template_name = "cashflow/listflow.html"
