"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

app_name = 'cashflow'

urlpatterns = [
    path('', views.CashflowListView.as_view(), name="flow-list"),
    path('flow-create/', views.CashFlowCreateView.as_view(), name="flow-create"),
    path('flow-update/<int:pk>/', views.CashFlowUpdateView.as_view(), name="flow-update"),
    path('flow-delete/<int:pk>/', views.CashFlowDeleteView.as_view(), name="flow-delete"),

    path('refrences/', views.refrence_data, name="refrence-list"),
    path('refrence-create/', views.refrence_data, name="refrence-create"),
    path('refrence-update/', views.refrence_data, name="refrence-update"),
    path('refrence-delete/', views.refrence_data, name="refrence-delete"),

    path('api/structure-data/', views.ajax_get_structure_data, name="api-structure-data")
]
