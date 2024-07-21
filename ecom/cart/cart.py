from store.models import Product, Profile

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
        # Get request
        self.request = request 
        
        #  Get the current session key if it exist
        cart = self.session.get('session_key')

        # if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        # if product_id not in self.cart:
            # self.cart[product_id] = {'price': str(product.price), 'quantity': 1}
        # else:
            # self.cart[product_id]['quantity'] += 1

        self.session.modified = True
        
        # Deal with logged in users
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # getting rid of single quotation marks in the python dictionary having the cart items i.e; {'4':2, '2':1} to {"4":2, "2":1}
            # this will help json to convert the string stored in the db back to a dictionary, key: remember json doesn't understand singlie quotation marks
            carty = str(self.cart).replace("\'", "\"")
            # save carty to the Profile model
            current_user.update(old_cart=carty)
            

    def cart_total(self):
        # Get product IDs from cart
        product_ids = self.cart.keys()
        # look up those keys in our database models
        products = Product.objects.filter(id__in=product_ids)
        # get quantities
        quantities = self.cart # this is going to return {'4':3, '2':4 }
        # start counting at zero
        total = 0
        # loop through products and get total
        for key, value in quantities.items():
            #  converting the key string to int
            key = int(key)
            # looping through our products
            for product in products:
                if product.id == key:
                    # check if product is on sale
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
        return total
             
    
    def __len__(self):
        return len(self.cart)
        # return sum(item['quantity'] for item in self.cart.values())

    def get_products(self):
        # get ids from cart
        product_ids = self.cart.keys()
        # use ids to look products in database model
        products = Product.objects.filter(id__in=product_ids)

        # return those looked up products
        return products

    def get_quantities(self):
        quantities = self.cart

        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # remember our cart is in the form of a dictionary {'4':3, '2':4 }

        # get cart
        # ourcart = self.cart

        # updating dictionary/cart
        # ourcart[product_id] = product_qty

        # the above can be simplified to:
        self.cart[product_id] = int(product_qty)

        # update the session with the updated cart
        self.session.modified = True
        
    def delete(self, product):
        product_id = str(product)
        
        # delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
            
            self.session.modified = True
