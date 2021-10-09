from django.shortcuts import get_object_or_404, render
from .session import Session
from django.http import JsonResponse
from ecommerce.apps.offert.models import Product


def basket_home(request):
    session = Session(request)
    print(request.POST)

    context = {
        'session': session
    }
    return render(request, "session/basket_home.html", context)


def add(request):
    session = Session(request)
    if request.method == 'POST':
        qty = request.POST.get('qty')
        product_id = request.POST.get('product_id')
        session.add(get_object_or_404(Product, id=product_id), qty=qty)

        context = {'qty': qty,
                   'product_id': product_id,
                   }
        return JsonResponse(context)
