from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)
    typeflow = models.ForeignKey('TypeFlow', null=True, blank=True, on_delete=models.SET_NULL, related_name='categories')
    supercategory = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

class StatusFlow(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TypeFlow(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CashFlow(models.Model):
    amount = models.DecimalField(max_digits=30, decimal_places=2)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(editable=True)

    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, related_name="cashflows")
    status = models.ForeignKey('StatusFlow', null=True, blank=True, on_delete=models.SET_NULL, related_name="cashflows")
    typeflow = models.ForeignKey('TypeFlow', null=True, blank=True, on_delete=models.SET_NULL, related_name="cashflows")

    def __str__(self):
        return str(self.amount)

    def save(self, *args, **kwargs):
        # для автозаполнения времени создания + сохранения возможности редактирования
        if not self.pk:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

