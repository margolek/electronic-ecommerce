

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
        print(qty)
        if product.price.in_sale:
            price = int(self.current_session[str(
                product.pk)]['qty'])*float(product.price.in_sale_price)
        elif product.price.day_product:
            price = int(self.current_session[str(
                product.pk)]['qty'])*float(product.price.day_product_price)
        else:
            price = int(self.current_session[str(
                product.pk)]['qty'])*float(product.price.regular)

        context = {
            'qty': qty,
            'price': str(price),
        }

        self.current_session[str(product.pk)] = context
        print(self.current_session)
        self.save()

    def save(self):
        self.session.modified = True

    def count_product(self):
        pass
