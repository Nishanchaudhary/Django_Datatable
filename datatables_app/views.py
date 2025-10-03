from django.shortcuts import render
from django.http import JsonResponse
from .models import Customer, Product
from django.db.models import Q
import math

def home(request):
    return render(request, 'home.html')

def customer_list(request):
    return render(request, 'customer_list.html')

def product_list(request):
    return render(request, 'product_list.html')


def get_customers_json(request):
    # Get DataTables parameters
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    
    # Total records count
    total_records = Customer.objects.count()
    
    # Apply search filter if exists
    if search_value:
        customers = Customer.objects.filter(
            Q(name__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(city__icontains=search_value)
        )
        filtered_records = customers.count()
    else:
        customers = Customer.objects.all()
        filtered_records = total_records
    
    # Apply pagination
    customers = customers.order_by('-id')[start:start + length]
    
    # Prepare data
    data = []
    for customer in customers:
        data.append({
            'id': customer.id,
            'name': customer.name,
            'email': customer.email,
            'phone': customer.phone or 'N/A',
            'city': customer.city or 'N/A',
            'country': customer.country or 'N/A',
            'created_at': customer.created_at.strftime('%Y-%m-%d'),
        })
    
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': data,
    })

def get_products_json(request):
    # Get DataTables parameters
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')
    
    # Total records count
    total_records = Product.objects.count()
    
    # Apply search filter if exists
    if search_value:
        products = Product.objects.filter(
            Q(name__icontains=search_value) |
            Q(category__icontains=search_value)
        )
        filtered_records = products.count()
    else:
        products = Product.objects.all()
        filtered_records = total_records
    
    # Apply pagination
    products = products.order_by('-id')[start:start + length]
    
    # Prepare data
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': float(product.price),
            'quantity': product.quantity,
            'is_available': 'Yes' if product.is_available else 'No',
            'created_at': product.created_at.strftime('%Y-%m-%d'),
        })
    
    return JsonResponse({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': filtered_records,
        'data': data,
    })

