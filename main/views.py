from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import Products, Users

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def product_list(request):
    # Проверка доступа (гость или авторизован)
    if request.GET.get('guest') == '1':
        request.session['guest'] = True
    else:
        request.session['guest'] = False

    if not request.user.is_authenticated and not request.session.get('guest'):
        return redirect('login')

    products = Products.objects.all()

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(supplier__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(article__icontains=search_query)
        )

    supplier_filter = request.GET.get('supplier', '')
    if supplier_filter:
        products = products.filter(supplier=supplier_filter)

    sort_by = request.GET.get('sort', '')
    if sort_by == 'quantity_asc':
        products = products.order_by('quantity')
    elif sort_by == 'quantity_desc':
        products = products.order_by('-quantity')

    all_suppliers = Products.objects.values_list('supplier', flat=True).distinct().order_by('supplier')

    return render(request, 'product_list.html', {
        'products': products,
        'search_query': search_query,
        'supplier_filter': supplier_filter,
        'sort_by': sort_by,
        'all_suppliers': all_suppliers,
    })

def product_add(request):
    return render(request, 'product_form.html')

def product_edit(request, pk):
    return render(request, 'product_form.html')

def product_delete(request, pk):
    return redirect('product_list')