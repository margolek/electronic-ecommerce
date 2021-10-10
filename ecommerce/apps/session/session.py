from ecommerce.apps.offert.models import Product
from decimal import Decimal
import numpy as np


class Session:
    """
    Class allow us communicate using django session framework (cookies)
    """

    def __init__(self, request):
        self.session = request.session
        current_session = self.session.get("session")
        if "session" not in self.session:
            current_session = self.session["session"] = {}
        self.current_session = current_session

    def add(self, product, qty):

        # Get product Price
        if product.price.in_sale:
            price = product.price.in_sale_price
        elif product.price.day_product:
            price = product.price.day_product_price
        else:
            price = product.price.regular

        context = {
            'qty': qty,
            'detail_price': str(price),
            'subtotal_price': int(qty)*float(price)
        }

        self.current_session[str(product.pk)] = context
        print(self.current_session)
        self.save()

    def get_total_price(self):
        return np.round(sum([self.current_session[i]['subtotal_price'] for i in self.current_session.keys()]), 2)

    def count_product(self):
        return len([i for i in self.current_session.keys()])

    def save(self):
        self.session.modified = True
