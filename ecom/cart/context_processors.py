from .cart import Cart

#  Create context processors so our Cart can work all pages of the site
def cart(request):
    # Return the default data from our Cart
    return {'cart': Cart(request)}