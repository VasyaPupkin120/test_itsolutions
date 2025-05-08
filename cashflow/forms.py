from django import forms
from .models import CashFlow, TypeFlow, Category, Subcategory, StatusFlow


class CreateUpdateCashFlowForm(forms.ModelForm):
    """
    Форма для создания и редактирования записи ДДС
    """
    created_at = forms.DateField(
        # вынужден указать здесь поле и параметр required чтобы браузер не требовал его заполнения
        required=False,
        label='Дата движения',
        widget=forms.DateInput(
            attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'created_at',
                'label': 'Дата создания'
            },
            format='%d.%m.%Y'
        )
    )
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
            # перекрыто объявлением поля в основном классе формы
            # 'created_at': forms.DateInput(attrs={
            #     'class': 'form-control',
            #     'type': 'date',
            #     'id': 'created_at',
            #     'format': '%d.%m.%Y',
            #     'required': False
            # }),
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
            # 'created_at': 'Дата движения',
            'typeflow': 'Тип',
            'category': 'Категория',
            'subcategory': 'Подкатегория',
            'status': 'Статус',
            'comment': 'Комментарий'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Преобразуем дату в формат пригодный для чтения браузером, для красивого выбора даты
        if self.instance and self.instance.pk:
            self.initial['created_at'] = self.instance.created_at.strftime('%Y-%m-%d')



class FilterCashFlowForm(forms.Form):
    """
    Форма для фильтрации списка ДДС.
    """
    start_date = forms.DateField(
        label='Начальная дата',
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'start_date'
            },
            format='%d.%m.%Y'
        )
    )
    end_date = forms.DateField(
        label='Конечная дата',
        required=False,
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'id': 'end_date'
            },
            format='%d.%m.%Y'
        )
    )
    typeflow = forms.ModelChoiceField(
        label='Тип',
        queryset=TypeFlow.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'typeflow'
            }
        )
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'category',
            }
        )
    )
    
    subcategory = forms.ModelChoiceField(
        label='Подкатегория',
        queryset=Subcategory.objects.none(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'subcategory',
            }
        )
    )
    status = forms.ModelChoiceField(
        label='Статус',
        queryset=StatusFlow.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'id': 'status'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Устанавливаем пустые значения по умолчанию
        self.fields['typeflow'].empty_label = "Тип"
        self.fields['category'].empty_label = "Категория"
        self.fields['subcategory'].empty_label = "Подкатегория"
        self.fields['status'].empty_label = "Статус"
        

class TypeflowCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = TypeFlow
        fields = ['name',]


class CategoryCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'typeflow']
    

class SubcategoryCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'supercategory']


class StatusflowCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusFlow
        fields = ['name', ]
