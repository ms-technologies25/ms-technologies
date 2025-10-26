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
    product_image_1 = models.ImageField(upload_to='product-images/')
    product_image_2 = models.ImageField(upload_to='product-images/', blank=True, null=True)
    latest_arrival = models.CharField(max_length=3, choices=LATEST_ARRIVAL_CHOICES, default='no')
    stock_status = models.CharField(max_length=20, choices=STOCK_STATUS_CHOICES, default='in_stock')

    def save(self, *args, **kwargs):
        for image_field in ['product_image_1', 'product_image_2']:
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

