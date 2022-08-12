import json
from .models import *

def cookieCart(request):
    try:
        # Store items in cart by retrieving from cookie.
        cart = json.loads(request.COOKIES["cart"])
        print("Cart: ", cart)
    except:
        # Exception handling for scenario where there is no cart cookie.
        cart = {}

    items = []
    # Exception handling for guest user.
    order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    cartItems = order['get_cart_items']

    for i in cart:
        # Exception handling for unavailable item due to old cookie.
        try:
            cartItems = cartItems + cart[i]["quantity"]

            product = Product.objects.get(id=i) # Store product
            total = (product.price * cart[i]["quantity"])

            order["get_cart_total"] = order["get_cart_total"] + total
            order["get_cart_items"] = order["get_cart_items"] + cart[i]["quantity"]

            item = {
                "product":{
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "imageURL": product.imageURL,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass
        
    return {"cartItems":cartItems, "order":order, "items":items}

def cartData(request):
    # Render cart for logged-in user
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False) # Get or create order
        items = order.orderitem_set.all() # Get all order items for parent order.
        cartItems = order.get_cart_items
    # Render cart for guest user
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]
    
    return {"cartItems":cartItems, "order":order, "items":items}

def guestOrder(request, data):
    print('User is not logged in.')

    print("COOKIES: ", request.COOKIES)
    name = data["form"]["name"]
    email = data["form"]["email"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    customer, created = Customer.objects.get_or_create(
        email = email,
    )

    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False,
    )

    for item in items:
        product = Product.objects.get(id = item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item["quantity"]
        )
        
    return customer, order
