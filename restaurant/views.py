import time
from django.shortcuts import render
import random

# global list of daily special items
special_items = [
    "Spaghetti",
    "Steak & Eggs",
    "Cheeseburger",
    "Pizza",
    "Caesar Salad",
]

special_items_prices = {
    "Spaghetti": 16.99,
    "Steak & Eggs": 23.99,
    "Cheeseburger": 19.99,
    "Pizza": 19.99,
    "Caesar Salad": 5.99,
}

# Create your views here.
def main(request):
    '''
    main : the view for the main page.
    This view simply directs the application to display the main.html template.
    '''
    return render(request, 'restaurant/main.html')

def order(request):
    '''
    order : the view for the ordering page. This view will need to create a “daily special” item (choose randomly from a list), and add it to the context dictionary for the page.
    Finally, delegate presentation to the order.html HTML template for display.
    '''
    # random special
    special = random.choice(special_items)
    context = {
        'special': special
    }
    return render(request, 'restaurant/order.html', context)

def confirmation(request):
    '''
    confirmation: the view to process the submission of an order, and display a confirmation page.
    This view must check the form data to determine which items have been ordered, and add these back to the context for the confirmation page. In addition, the view must calculate the total price for the order – keep it simple, but nonetheless add the items up; include this total in the order confirmation.
    Finally, delegate presentation to the confirmation.html HTML template for display.
    '''
    if request.method == 'POST':
        # gather data from the form
        customer_name = request.POST['customer_name']
        customer_phone = request.POST['customer_phone']
        customer_email = request.POST['customer_email']
        special_instructions = request.POST.get('special_instructions', 'With no special instructions.')

        # get the order items
        order_items = []

        order_special = request.POST.get('special')
        if order_special:
            order_items.append({'item': order_special})

        if request.POST.get('spaghetti'):
            order_items.append({'item': 'Spaghetti'})
        if request.POST.get('steak_eggs'):
            order_items.append({'item':'Steak & Eggs'})
        if request.POST.get('cheeseburger'):
            order_items.append({'item': 'Cheeseburger'})
        if request.POST.get('pizza'):
            toppings = request.POST.getlist('toppings')
            print(toppings)
            order_items.append({'item': 'Pizza', 'toppings': toppings})

        if request.POST.get('caesar_salad'):
            order_items.append({'item': 'Caesar Salad'})

        # calc the prices
        total_cost = 0
        for item in order_items:
            total_cost += special_items_prices[item['item']]

        unix_time = time.time() + random.randint(1800, 3600)  
        prep_time = time.strftime('%H:%M', time.localtime(unix_time)) 
        context = {
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'order_items': order_items,
            'special_instructions': special_instructions, 
            'total_cost': total_cost,
            'prep_time': prep_time
        }

        return render(request, 'restaurant/confirmation.html', context)