from django.shortcuts import render,redirect
import requests
import json
from .forms import ProductForm
from .models import Product
from django.shortcuts import get_object_or_404

def home(request):
    try:
        # Replace 'https://dummyjsonapi.com/products' with your DummyJSON API endpoint
        url = 'https://dummyjson.com/products'
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

        products_data = response.json().get('products', [])

        return render(request, 'store/upload.html', {'products_data': products_data})
    
    except requests.RequestException as e:
        # Handle API request failure
        error_message = f"Failed to fetch data from API: {e}"
        return render(request, 'store/upload.html', {'error_message': error_message})

def login(request):
    return render(request,'store/login.html')

def signup(request):
    return render(request,'store/signup.html')

def basepage(request):
    return render(request,'store/base.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})



def edit_product(request,id):
    product = get_object_or_404(Product,id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form})




def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        # If it's a POST request, delete the product
        product.delete()
        return redirect('product_list')
    # If it's not a POST request, you may choose to render a confirmation page or redirect
    return render(request, 'store/delete_product.html', {'product': product})






    

