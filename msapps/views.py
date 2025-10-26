from django.shortcuts import render, get_object_or_404
from msapps.models import product, Category
import json
from math import ceil

def shop(request, category=None):
    allProds = []

    if category:
        category_obj = Category.objects.filter(slug=category, is_active=True).first()
        if not category_obj:
            cat = category.replace("-", " ").title()
            return render(request, "shop.html", {
                'message': f"No products available in the '{cat}' category. Please check back later!"
            })
        prod = product.objects.filter(product_category=category_obj)
        if prod.exists():
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
        else:
            cat = category.replace("-", " ").title()
            return render(request, "shop.html", {
                'message': f"No products available in the '{cat}' category. Please check back later!"
            })
    else:
        categories = Category.objects.filter(is_active=True)
        for cat in categories:
            prod = product.objects.filter(product_category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allProds.append([prod, range(1, nSlides), nSlides])
    
    data = {
        'allProds': allProds,
        'message': None if allProds else "No products available at the moment. Please check back later!"
    }
    return render(request, "shop.html", data)

def productDetails(request, id):
    prod = get_object_or_404(product, id=id)
    
    data = {
        'product': prod,
    }
    return render(request, "quickview.html", data)