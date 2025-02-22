from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm  # Ensure you have this form
from django.contrib.auth.decorators import login_required

@login_required
def products(request):
    all_products = Product.objects.all()  # Fetch all products from the database
    return render(request, 'products/products.html', {'products': all_products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')  # Redirect to the products list
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':  # Confirm deletion before proceeding
        product.delete()
        return redirect('products')

    return render(request, 'products/delete_product.html', {'product': product})
