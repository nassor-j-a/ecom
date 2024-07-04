from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.


def cart_summary(request):
    return render(request, "cart_summary.html", {})


def cart_add(request):
    # Get the cart
    cart = Cart(request)
    # test for POST

    if request.POST.get('action') == 'post':
    #     # get stuff
    #     product_id = int(request.POST.get('product_id'))

    #     # lookup product in the DB
    #     product = get_object_or_404(Product, id=product_id)

    #     # save to session
    #     cart.add(product=product)

    #     # Get cart quantity
    #     cart_quantity = cart.__len__()
    #     response = JsonResponse({'qty': cart_quantity})
    #     print(f"Added product {
    #           product.name} to cart. New cart quantity: {cart_quantity}")

    #     # Return response
    #     # response = JsonResponse({'Product Name: ': product.name })

    #     return response

        try:
            product_id = int(request.POST.get('product_id'))
            product = get_object_or_404(Product, id=product_id)
            cart.add(product=product)

            cart_quantity = cart.__len__()
            response = JsonResponse({'qty': cart_quantity})
            print(f"Added product {
                product.name} to cart. New cart quantity: {cart_quantity}")
            return response

        except ValueError:
            return JsonResponse({'error': 'Invalid product ID'}, status=400)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
    
    return JsonResponse({'error': 'Invalid action'}, status=400)


def cart_delete(request):
    pass


def cart_update(request):
    pass
