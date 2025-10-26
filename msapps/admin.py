from django.contrib import admin
from msapps.models import product, Category, ProductStock
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from .utils import deduct_stock_for_order
from msapps.models import contact

admin.site.register(contact)

class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1
    fields = ('size', 'color', 'quantity')
    verbose_name = 'Product Stock'
    verbose_name_plural = 'Product Stock'


@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_price', 'stock_status', 'latest_arrival')
    list_filter = ('product_category', 'stock_status', 'latest_arrival')
    search_fields = ('product_name', 'product_desc')
    list_editable = ('stock_status',)
    inlines = [ProductStockInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('product_name', 'product_category', 'product_price', 'product_desc')
        }),
        ('Product Status', {
            'fields': ('stock_status', 'latest_arrival')
        }),
        ('Images', {
            'fields': ('product_image_1', 'product_image_2', 'product_image_3', 'product_image_4', 'product_image_5')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    
