from decimal import Decimal
from django.conf import settings
from .models import Productmaster, offers


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': quantity,
                'name': product.product_name,
                'image': str(product.image_1.url),
            }
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    # Inside the get_cart_items method of cart.py
    def get_cart_items(self):
        product_ids = self.cart.keys()
        products = Productmaster.objects.filter(product_id__in=product_ids)

        cart_items = []
        for product in products:
            cart_item = {
                'product': product,
                'quantity': self.cart[str(product.product_id)]['quantity'],
                'name': self.cart[str(product.product_id)]['name'],
                'image': self.cart[str(product.product_id)]['image'],
            }

            # Get discount price from the Offer database
            offer = offers.objects.filter(product=product).first()
            discount_price = offer.discountprice if offer else None

            # Check if the product has a discount price
            if discount_price:
                cart_item['price'] = Decimal(discount_price)
                cart_item['total'] = Decimal(discount_price) * Decimal(cart_item['quantity'])
            else:
                cart_item['price'] = Decimal(product.sales_price)
                cart_item['total'] = Decimal(product.sales_price) * Decimal(cart_item['quantity'])

            cart_items.append(cart_item)

        return cart_items

    def update(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
