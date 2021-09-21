from .models import Product, Price, Images


class Offert:

    def __init__(self):
        try:
            self.price_day = Price.objects.get(day_product=True)
            self.day_product = Product.objects.get(
                id=self.price_day.product_id)
            self.day_product_image = Images.objects.filter(
                product=self.price_day.product_id, default=True).get()
        except:
            self.price_day = []
            self.day_product = []
            self.day_product_image = []

    def day_product_percentage(self):
        try:
            percentage = round(((self.price_day.regular-self.price_day.day_product_price) /
                                self.price_day.regular)*100, 0)
        except:
            percentage = []
        return percentage

    def available_quantity(self):
        try:
            available_qty = round((self.day_product.quantity/100)*100, 0)
        except:
            available_qty = []
        return available_qty

    def save(self):
        pass
