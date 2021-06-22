from django import template

register = template.Library()

@register.filter(name = 'is_in_cart')
def is_in_cart(fd, cart):
    
    keyss = cart.keys()
    print(fd)
    for id in keyss:
        if int(id) == fd.id:
            return True
    return False
    print(fd, cart)

@register.filter(name = 'cart_quantity')
def cart_quantity(fd, cart):
    
    keyss = cart.keys()
    # print(fd)
    for id in keyss:
        if int(id) == fd.id:
            return cart.get(id)
    return 0
    # print(fd, cart)

@register.filter(name = 'price_total')
def price_total(fd, cart):
    return fd.food_price * cart_quantity(fd, cart)
    

@register.filter(name = 'total_cart_price')
def total_cart_price(foods, cart):
    sum = 0;
    for p in foods:
        sum += price_total(p, cart)
    return sum
    

@register.filter(name = 'multiply')
def multiply(number, number1):
    return number * number1
    