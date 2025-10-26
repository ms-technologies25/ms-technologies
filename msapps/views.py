from django.shortcuts import render, get_object_or_404
from msapps.models import product, Category, ProductStock
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
    # Prefer variant-based options from ProductStock; fallback to comma fields
    variant_qs = ProductStock.objects.filter(product=prod, quantity__gt=0)
    if variant_qs.exists():
        colors = sorted(set(v.color for v in variant_qs))
        sizes = sorted(set(v.size for v in variant_qs))
        options_by_color = {}
        quantities = {}
        for v in variant_qs:
            options_by_color.setdefault(v.color, set()).add(v.size)
            quantities[f"{v.color}|{v.size}"] = v.quantity
        # Convert sets to lists for JSON serialization
        options_by_color = {c: sorted(list(sizes_set)) for c, sizes_set in options_by_color.items()}
    else:
        colors = [c.strip() for c in (prod.product_color or '').split(',') if c.strip()]
        sizes = [s.strip() for s in (prod.product_size or '').split(',') if s.strip()]
        options_by_color = {}
        quantities = {}

    data = {
        'product': prod,
        'colors': colors,
        'sizes': sizes,
        'variant_options_by_color_json': json.dumps(options_by_color),
        'variant_quantities_json': json.dumps(quantities),
    }
    return render(request, "quickview.html", data)