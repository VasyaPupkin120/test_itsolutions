from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    typeflow = models.ForeignKey('TypeFlow', on_delete=models.PROTECT, related_name='categories', verbose_name="Тип движения")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")
    supercategory = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='subcategories', verbose_name="Надкатегория")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"

    def __str__(self):
        return self.name


class StatusFlow(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.name


class TypeFlow(models.Model):
    name = models.CharField(max_length=50, verbose_name="Название")

    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"

    def __str__(self):
        return self.name


class CashFlow(models.Model):
    amount = models.DecimalField(max_digits=30, decimal_places=2, verbose_name="Сумма")
    comment = models.TextField(null=True, blank=True, verbose_name="Комментарий")
    created_at = models.DateField(editable=True, verbose_name="Дата движения")
    typeflow = models.ForeignKey('TypeFlow', on_delete=models.PROTECT, related_name="cashflows", verbose_name="Тип движения")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name="cashflows", verbose_name="Категория")
    subcategory = models.ForeignKey('Subcategory', on_delete=models.PROTECT, related_name="cashflows", verbose_name="Подкатегория")
    status = models.ForeignKey('StatusFlow', on_delete=models.PROTECT, related_name="cashflows", verbose_name="Статус")
    
    class Meta:
        verbose_name = "Движение средств"
        verbose_name_plural = "Движения средств"
        ordering = ["-created_at", "-amount"]

    def __str__(self):
        return str(self.amount)

    def clean(self):
        super().clean()
        if self.category.typeflow != self.typeflow:
            raise ValidationError({'category': f"Категория {self.category.name} не принадлежит типу {self.typeflow.name}"})
        if self.subcategory.supercategory != self.category:
            raise ValidationError({'subcategory': f"Подкатегория {self.subcategory.name} не принадлежит категории {self.category.name}"})

    def save(self, *args, **kwargs):
        # для автозаполнения времени создания + сохранения возможности редактирования
        if not self.pk:
            if not self.created_at:
                self.created_at = timezone.now()

        # для запуска валидации в любом случае
        self.full_clean()
        super().save(*args, **kwargs)

