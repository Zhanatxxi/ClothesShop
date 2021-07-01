from django_filters.rest_framework import FilterSet
import django_filters

from order.models import Order
from .models import Product


class ProductFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('fk_product', 'title', 'description', 'price_from', 'price_to')


class OrderFilter(FilterSet):
    total_sum_from = django_filters.NumberFilter(field_name='total_sum', lookup_expr='gte')
    total_sum_to = django_filters.NumberFilter(field_name='total_sum', lookup_expr='lte')
    created_at = django_filters.DateFromToRangeFilter(field_name='created_ad')
    product = django_filters.CharFilter(field_name='products__product__title', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ('total_sum_from',
                  'total_sum_to',
                  'created_at',
                  'product')


