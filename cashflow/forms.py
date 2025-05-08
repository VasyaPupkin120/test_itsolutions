from django import forms
from .models import CashFlow, TypeFlow, Category, Subcategory, StatusFlow


class CreateUpdateCashFlowForm(forms.ModelForm):
    """
    Форма для редактирования записи ДДС
    """
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
            'created_at': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'created_at',
                'required': True,
                'format': '%d.%m.%Y'
            }),
            'typeflow': forms.Select(attrs={
                'class': 'form-control',
                'id': 'typeflow',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
                'id': 'category',
                'required': True,
            }),
            'subcategory': forms.Select(attrs={
                'class': 'form-control',
                'id': 'subcategory',
                'required': True,
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
        # Преобразуем дату в формат пригодный для чтения html, для красивого выбора даты
        if self.instance and self.instance.pk:
            self.initial['created_at'] = self.instance.created_at.strftime('%Y-%m-%d')
