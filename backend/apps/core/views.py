from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def catalog(request):
    return render(request, 'catalog.html')


def about(request):
    return render(request, 'about.html')


def contacts(request):
    return render(request, 'contacts.html')


def find_us(request):
    return render(request, 'find-us.html')


def product_detail(request, pk):
    return render(request, 'product_detail.html', {'product_id': pk})


