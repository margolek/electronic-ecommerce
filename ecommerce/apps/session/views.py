from django.shortcuts import get_object_or_404, render
from .session import Session
from django.http import JsonResponse
from ecommerce.apps.offert.models import Product, Images
from django.contrib import messages


def basket_home(request):
    session = Session(request)
    total_price = session.get_total_price()
    product_ids = [i for i in session.current_session.keys()]
    products = Product.objects.filter(id__in=product_ids)

    for product in products:
        session.current_session[str(product.id)]['product'] = product

    context = {
        'session': session,
        'total_price': total_price,
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


def update(request):
    session = Session(request)
    if request.method == 'POST':
        pk = request.POST.get('pk')
        id_type = request.POST.get('id_type')
        qty = request.POST.get('qty')
        qty = int(qty)
        product = get_object_or_404(Product, id=int(pk))
        product_qty_store = product.quantity
        limit = False
        if id_type == 'add-item':
            if int(qty) + 1 <= int(product_qty_store):
                qty += 1
                session.add(product, qty)
            else:
                limit = True
        if id_type == 'remove-item':
            if int(qty) - 1 > 0:
                qty -= 1
                session.add(product, qty)
    context = {
        'pk': pk,
        'id_type': id_type,
        'qty': qty,
        'price': session.current_session[pk]['subtotal_price'],
        'limit': limit,

    }
    print(context)
    return JsonResponse(context)
