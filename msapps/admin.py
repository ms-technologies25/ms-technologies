from django.contrib import admin
from msapps.models import product, Category
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from msapps.models import contact

admin.site.register(contact)

@admin.register(product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_category', 'product_price', 'stock_status', 'latest_arrival')
    list_filter = ('product_category', 'stock_status', 'latest_arrival')
    search_fields = ('product_name', 'product_desc')
    list_editable = ('stock_status',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('product_name', 'product_category', 'product_price', 'product_desc')
        }),
        ('Product Status', {
            'fields': ('stock_status', 'latest_arrival')
        }),
        ('Images', {
            'fields': ('product_image_1', 'product_image_2')
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    
