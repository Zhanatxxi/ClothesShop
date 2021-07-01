from django.contrib import admin
from .models import *


class PostImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 5
    min_num = 1


@admin.register(Product)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline, ]


admin.site.register(Category)




