from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from multiselectfield import MultiSelectField

from account.models import User


class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    SIZE_CHOICES = (
        ('XC', 'XC'),
        ('XL', 'XL'),
        ('L', 'L'),
        ('M', 'M'),
        ('S', 'S'),
    )
    fk_product = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
    title = models.CharField(max_length=150)
    description = models.TextField()
    size = MultiSelectField(max_length=2, choices=SIZE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.SmallIntegerField()

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to='product', blank=True, null=True)


class ClickLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    is_like = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
    favorite = models.BooleanField(default=False)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['author', 'product']



