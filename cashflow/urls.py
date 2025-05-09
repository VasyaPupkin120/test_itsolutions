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

    path('refrence-create/typeflow/', views.RefrenceTypeflowCreateView.as_view(), name="refrence-typeflow-create"),
    path('refrence-update/typeflow/<int:pk>/', views.RefrenceTypeflowUpdateView.as_view(), name="refrence-typeflow-update"),
    path('refrence-delete/typeflow/<int:pk>/', views.RefrenceTypeflowDeleteView.as_view(), name="refrence-typeflow-delete"),

    path('refrence-create/category/', views.RefrenceCategoryCreateView.as_view(), name="refrence-category-create"),
    path('refrence-update/category/<int:pk>/', views.RefrenceCategoryUpdateView.as_view(), name="refrence-category-update"),
    path('refrence-delete/category/<int:pk>/', views.RefrenceCategoryDeleteView.as_view(), name="refrence-category-delete"),

    path('refrence-create/subcategory/', views.RefrenceSubcategoryCreateView.as_view(), name="refrence-subcategory-create"),
    path('refrence-update/subcategory/<int:pk>/', views.RefrenceSubcategoryUpdateView.as_view(), name="refrence-subcategory-update"),
    path('refrence-delete/subcategory/<int:pk>/', views.RefrenceSubcategoryDeleteView.as_view(), name="refrence-subcategory-delete"),

    path('refrence-create/statusflow/', views.RefrenceStatusflowCreateView.as_view(), name="refrence-statusflow-create"),
    path('refrence-update/statusflow/<int:pk>/', views.RefrenceStatusflowUpdateView.as_view(), name="refrence-statusflow-update"),
    path('refrence-delete/statusflow/<int:pk>/', views.RefrenceStatusflowDeleteView.as_view(), name="refrence-statusflow-delete"),

    path('api/get-structure-data/', views.api_get_structure_data, name="api-get-structure-data")
]
