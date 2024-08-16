from django.shortcuts import render
from cart.cart import Cart

from payment.forms import ShippingForm
from payment.models import ShippingAddress



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

    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as authenticated user
        # Shipping User
        shipping_user = ShippingAddress.objects.get(user=request.user)
        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form":shipping_form })
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form":shipping_form })
