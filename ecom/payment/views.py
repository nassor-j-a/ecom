from django.shortcuts import render, get_object_or_404
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
    # Get specific product's quantities
    quantities = cart.get_quantities()
    # Calculate totals
    totals = cart.cart_total()

    # Prepare shipping form
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.filter(user=request.user).first()
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)

    # Render checkout page
    context = {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    }
    return render(request, "payment/checkout.html", context)


def billing_info(request):
 pass