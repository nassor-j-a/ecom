from django.shortcuts import render
from cart.cart import Cart


# Create your views here.
def payment_success(request):
 return render(request, "payment/payment_success.html", {})


def checkout(request):
    # Get the cart
    cart = Cart(request)
    # Get all products from the cart
    cart_products = cart.get_products()
    
    # get specifi product's quantites
    quantities = cart.get_quantities()
    
    totals =  cart.cart_total()
    
    return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals })