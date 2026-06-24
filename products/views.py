from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404

from .models import Product
from .forms import ProductForm
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import HttpResponse
import openpyxl
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

#Login
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(request, user)

            return redirect('dashboard')

    return render(request,'login.html')

#Logout
def user_logout(request):

    logout(request)

    return redirect('login')


#Export to Excel
@login_required
def export_products_excel(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active

    sheet.title = 'Products'

    headers = [
        'ID',
        'Product Name',
        'Category',
        'Price',
        'Quantity',
        'Description',
        'Manufacture Date',
        'Expiry Date'
    ]

    sheet.append(headers)

    products = Product.objects.filter(
        is_deleted=False
    )

    for product in products:

        sheet.append([

            product.id,
            product.product_name,
            product.category,
            float(product.price),
            product.quantity,
            product.description,
            str(product.manufacture_date),
            str(product.expiry_date)

        ])

    response = HttpResponse(
        content_type=
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = (
        'attachment; filename=products.xlsx'
    )

    workbook.save(response)

    return response



# CREATE
@login_required
def product_create(request):

    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:
        form = ProductForm()

    return render(request,'product_form.html',{'form': form})

#Dashboard
@login_required
def dashboard(request):

    total_products = Product.objects.count()

    active_products = Product.objects.filter(
        is_deleted=False
    ).count()

    deleted_products = Product.objects.filter(
        is_deleted=True
    ).count()

    total_quantity = Product.objects.filter(
        is_deleted=False
    ).aggregate(
        Sum('quantity')
    )['quantity__sum'] or 0

    inventory_value = 0

    products = Product.objects.filter(
        is_deleted=False
    )

    for product in products:

        inventory_value += (
            product.price * product.quantity
        )

    context = {

        'total_products': total_products,
        'active_products': active_products,
        'deleted_products': deleted_products,
        'total_quantity': total_quantity,
        'inventory_value': inventory_value,
    }

    return render(request,'dashboard.html',context)

# READ
from django.db.models import Q
@login_required
def product_list(request):

    search = request.GET.get('search')

    products = Product.objects.filter(
        is_deleted=False
    )

    if search:

        products = products.filter(

            Q(product_name__icontains=search) |
            Q(category__icontains=search)

        )

    # Pagination starts here

    paginator = Paginator(products, 5)

    page_number = request.GET.get('page')

    products = paginator.get_page(page_number)

    # Pagination ends here

    context = {
        'products': products,
        'search': search
    }

    return render(
        request,
        'product_list.html',
        context
    )


# UPDATE
@login_required
def product_update(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():
            form.save()
            return redirect('product_list')

    else:

        form = ProductForm(
            instance=product
        )

    return render(request,'product_form.html',{'form': form})


# DELETE
@login_required
def product_delete(request, id):

    product = Product.objects.get(id=id)

    product.is_deleted = True

    product.save()

    return redirect('product_list')


#Deleted products
@login_required
def deleted_products(request):

    products = Product.objects.filter(
        is_deleted=True
    )

    return render(request,'deleted_products.html',{'products': products})


#Restore
@login_required
def restore_product(request, id):

    product = Product.objects.get(id=id)

    product.is_deleted = False

    product.save()

    return redirect('deleted_products')