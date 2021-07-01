from django.db import models

from account.models import User
from products.models import Product


class StatusChoices(models.TextChoices):
    new = ('new', 'Новый')
    in_progress = ('in_progress', 'В обработке')
    done = ('done', 'Выполнен')
    canceled = ('canceled', 'Отменён')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='orders')
    products = models.ManyToManyField(Product, through='OrderItems')
    status = models.CharField(max_length=15, choices=StatusChoices.choices)
    total_sum = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='orders')
    quantity = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['order', 'product']
