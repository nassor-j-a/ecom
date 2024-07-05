from store.models import Product

# class Cart():
#     # initialize the cart class
#     def __init__(self, request):
#         self.session = request.session
        
#         #  Get the current session key if it exist
#         cart = self.session.get('session_key')
        
#         # if the user is new, no session key! Create one!
#         if 'session_key' not in request.session:
#             cart = self.session['session_key'] = {}
            
#         # Make sure that Cart is available on all pages of site
#         self.cart = cart
        
#     #     self.items = []

#     def add(self, product):
#         product_id = str(product.id)
        
#         # logic 
#         if product_id not in self.cart:
#             # self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
#             pass
#         else:
#             self.cart[product_id] = {'price': str(product.price),}
        
#         self.session.modified = True
        
#     def __len__(self):
#         return sum(item['quantity'] for item in self.cart.values())


#     # def remove(self, product):
#     #     self.items.remove(product)

#     # def total(self):
#     #     return sum([product.price for product in self.items])


class Cart():
    # initialize the cart class
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        
        if product_id not in self.cart:
            self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
        else:
            self.cart[product_id]['quantity'] += 1
        
        self.session.modified = True
        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_products(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # use ids to look products in database model
        products = Product.objects.filter(id__in=product_ids)
        
        # return those looked up products
        return products
        