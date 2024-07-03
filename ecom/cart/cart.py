class Cart():
    # initialize the cart class
    def __init__(self, request):
        self.session = request.session
        
        #  Get the current session key if it exist
        cart = self.session.get('session_key')
        
        # if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure that Cart is available on all pages of site
        self.cart = cart
        
    #     self.items = []

    def add(self, product):
        product_id = str(product.id)
        
        # logic 
        if product_id not in self.cart:
            # self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
            pass
        else:
            self.cart[product_id] = {'price': str(product.price),}
        
        self.session.modified = True

    # def remove(self, product):
    #     self.items.remove(product)

    # def total(self):
    #     return sum([product.price for product in self.items])