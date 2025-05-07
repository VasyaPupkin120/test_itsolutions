from django import forms
from .models import CashFlow, TypeFlow, Category, Subcategory, StatusFlow

# class CashFlowForm(forms.ModelForm):
#     class Meta:
#         model = CashFlow
#         fields = ['amount', 'comment', 'typeflow', 'category', 'subcategory', 'status']
#         widgets = {
#             'comment': forms.Textarea(attrs={'rows': 3}),
#         }
#     
#     def clean_amount(self):
#         amount = self.cleaned_data['amount']
#         if amount <= 0:
#             raise forms.ValidationError("Сумма должна быть положительной")
#         return amount



class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = ['amount', 'created_at', 'typeflow', 'category', 'subcategory', 'status', 'comment']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'id': 'amount',
                'required': True
            }),
            'created_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'id': 'created_at',
                'required': True,
            }),
            'typeflow': forms.Select(attrs={
                'class': 'form-control',
                'id': 'typeflow',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'disabled': True,
                'id': 'category',
                'required': True
            }),
            'subcategory': forms.Select(attrs={
                'class': 'form-control',
                'disabled': True,
                'id': 'subcategory',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-control',
                'id': 'status',
                'required': True
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'comment',
                'rows': 2
            }),
        }
        labels = {
            'amount': 'Сумма (руб)',
            'created_at': 'Дата движения',
            'typeflow': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'status': 'Статус',
            'comment': 'Комментарий'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Преобразуем DateTime в формат для datetime-local
        if self.instance and self.instance.pk and self.instance.created_at:
            self.initial['created_at'] = self.instance.created_at.strftime('%Y-%m-%dT%H:%M')
        
        # Устанавливаем пустые значения по умолчанию для select
        self.fields['typeflow'].empty_label = "Выберите тип"
        self.fields['category'].empty_label = "Сначала выберите тип"
        self.fields['subcategory'].empty_label = "Сначала выберите категорию"
        self.fields['status'].empty_label = "Выберите статус"
        
        # Если форма инициализируется для существующего объекта
        if self.instance and self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(typeflow=self.instance.typeflow)
            self.fields['category'].widget.attrs.pop('disabled', None)
            
            self.fields['subcategory'].queryset = Subcategory.objects.filter(supercategory=self.instance.category)
            self.fields['subcategory'].widget.attrs.pop('disabled', None)
