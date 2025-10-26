from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User
import json
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from tinymce.models import HTMLField

# Create your models here.

class contact(models.Model):
    contact_name= models.CharField(max_length = 150, verbose_name="Name")
    contact_email=models.CharField(max_length=150, verbose_name="Email")
    contact_subject=models.CharField(max_length = 500, verbose_name="Subject")
    contact_message=models.CharField(max_length = 1500, verbose_name="Message")

    def __str__(self):
        return self.contact_subject

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    image = models.ImageField(upload_to='category-images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class product(models.Model):
    LATEST_ARRIVAL_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    product_category = models.ForeignKey(Category, related_name='products', on_delete=models.PROTECT, null=True, blank=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    product_desc = HTMLField()
    # Kept for backward compatibility with existing data entry; now optional.
    # New stock tracking uses ProductStock rows below.
    product_color = models.TextField(blank=True, default="")
    product_size = models.TextField(blank=True, default="")
    product_image_1 = models.ImageField(upload_to='product-images/')
    product_image_2 = models.ImageField(upload_to='product-images/')
    product_image_3 = models.ImageField(upload_to='product-images/')
    product_image_4 = models.ImageField(upload_to='product-images/')
    product_image_5 = models.ImageField(upload_to='product-images/')
    latest_arrival = models.CharField(max_length=3, choices=LATEST_ARRIVAL_CHOICES, default='no')
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')

    def save(self, *args, **kwargs):
        for image_field in ['product_image_1', 'product_image_2', 'product_image_3', 'product_image_4', 'product_image_5']:
            image = getattr(self, image_field)
            if image and not image.closed:
                img = Image.open(image)
                img = img.convert("RGB")
                output = BytesIO()
                
                max_size = (1080, 1080)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                img.save(output, format='JPEG', quality=100)
                output.seek(0)
                setattr(self, image_field, ContentFile(output.read(), image.name))

        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name

    def total_stock_quantity(self):
        total = sum(
            s.quantity for s in getattr(self, 'stocks', []).all()
        ) if hasattr(self, 'stocks') else sum(
            s.quantity for s in ProductStock.objects.filter(product=self)
        )
        return total

    def update_stock_status_from_stocks(self):
        total = self.total_stock_quantity()
        new_status = 'out_of_stock' if total <= 0 else 'in_stock'
        if self.stock_status != new_status:
            self.stock_status = new_status
            self.save(update_fields=['stock_status'])


class ProductStock(models.Model):
    SIZE_MAX_LEN = 20
    COLOR_MAX_LEN = 30

    product = models.ForeignKey(product, on_delete=models.CASCADE, related_name='stocks')
    size = models.CharField(max_length=SIZE_MAX_LEN)
    color = models.CharField(max_length=COLOR_MAX_LEN)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("product", "size", "color")
        verbose_name = "Product Stock"
        verbose_name_plural = "Product Stock"

    def __str__(self):
        return f"{self.product.product_name} - {self.color}/{self.size} ({self.quantity})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # After saving, update parent product stock status
        self.product.update_stock_status_from_stocks()