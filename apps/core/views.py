from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def product_detail(request, pk):
    return render(request, 'product_detail.html', {'product_id': pk})


