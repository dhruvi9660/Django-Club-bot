from __future__ import unicode_literals

from django.shortcuts import render,HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
#from shopping_cart.models import Order
from .models import Gym, Order_occasion, OrderItem_occasion, Product, occasion, Order_gym
from .models import Order
from .models import Profile
from .models import OrderItem, Order, Transaction
from django.urls import reverse
import random
import string
from datetime import date
import datetime
from myapp.forms import occasionForm



def index(request):
    return render(request, 'myapp/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'your account has been created! you can now login!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def menupage(request):
    return render(request, 'myapp/menupage.html')
# Create your views here.

def swimmingplan(request):
    return render(request, 'myapp/swimmingplan.html')


def contact(request):
    name=''
    email=''
    comment=''


    form= ContactForm(request.POST or None) #we have imported it from forms.py
    if form.is_valid():
        name= form.cleaned_data.get("name")
        email= form.cleaned_data.get("email")
        comment=form.cleaned_data.get("comment")
        receive = 'clubbot102@gmail.com' #this is the email of the admin where all the queries are redirected to

        if request.user.is_authenticated:
            subject= str(request.user) + "'s Comment"
        else:
            subject= "New Query From Customer"


        comment= name + " with the email, " + email + ", sent the following message:\n\n" + comment;
        send_mail(subject, comment, email,[receive])


        context= {'form': form}

        return render(request, 'myapp/contact.html', context)

    else:
        context= {'form': form}
        return render(request, 'myapp/contact.html', context)


@login_required
def profile(request):
    return render(request, 'myapp/profile.html')

@login_required
def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "myapp/product_list.html", context)

from django.shortcuts import render, get_object_or_404

def generate_order_id():
    date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
    rand_str = "".join([random.choice(string.digits) for count in range(3)])
    return date_str + rand_str

def my_profile(request):
	my_user_profile = Profile.objects.filter(user=request.user).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	context = {
		'my_orders': my_orders
	}

	return render(request, "myapp/profile.html", context)

@login_required()
def add_to_cart(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product in request.user.profile.ebooks.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('product-list')) 
    # create orderItem of the selected product
    order_item, status = OrderItem.objects.get_or_create(product=product)
    # create order associated with the user
    user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('product-list'))


@login_required()
def delete_from_cart(request, item_id):
    item_to_delete = OrderItem.objects.filter(pk=item_id)
    if item_to_delete.exists():
        item_to_delete[0].delete()
        messages.info(request, "Item has been deleted")
    return redirect(reverse('order_summary'))

def get_user_pending_order(request):
    # get order for the correct user
    user_profile = get_object_or_404(Profile, user=request.user)
    order = Order.objects.filter(owner=user_profile, is_ordered=False)
    if order.exists():
        # get the only order in the list of filtered orders
        return order[0]
    return 0


@login_required()
def order_details(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'myapp/order_summary.html', context)

@login_required()
def checkout(request, **kwargs):
    

    return render(request, 'myapp/checkout.html')

@login_required()
def order_details1(request, **kwargs):
    existing_order = get_user_pending_order(request)
    context = {
        'order': existing_order
    }
    return render(request, 'myapp/checkout.html', context)

from django.http import HttpResponse
from django.views.generic import View
 
#importing get_template from loader
from django.template.loader import get_template
 
#import render_to_pdf from util.py 
from .utils import render_to_pdf 
 
#Creating our view, it is a class based view
class GeneratePdf(View):
     def get(self, request, *args, **kwargs):
        existing_order = get_user_pending_order(request)
        context = {
            'order': existing_order
        }
        #getting the template
        pdf = render_to_pdf('myapp/invoice.html',context)
         
         #rendering the template
        return HttpResponse(pdf, content_type='application/pdf')    

@login_required
def occ_form(request):
    form1  = occasionForm()

    if request.method == 'POST':
        form1 = occasionForm(request.POST)
        if form1.is_valid:
            form1.save()
    return render(request,'myapp/occasion_details.html',{'form':form1})
    
    

@login_required
def occasion_product(request):
    object_list = occasion.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "myapp/occasion_product.html", context)

@login_required()
def add_to_cart_occasion(request, **kwargs):
    # get the user profile
    user_profile = get_object_or_404(Profile, user=request.user)
    # filter products by id
    product1 = occasion.objects.filter(id=kwargs.get('item_id', "")).first()
    # check if the user already owns this product
    if product1 in request.user.profile.ebooks.all():
        messages.info(request, 'You already own this ebook')
        return redirect(reverse('occasion_product')) 
    # create orderItem of the selected product
    order_item, status = OrderItem_occasion.objects.get_or_create(product=product1)
    # create order associated with the user
    user_order, status = Order_occasion.objects.get_or_create(owner=user_profile, is_ordered=False)
    user_order.items.add(order_item)
    if status:
        # generate a reference code
        user_order.ref_code = generate_order_id()
        user_order.save()

    # show confirmation message and redirect back to the same page
    messages.info(request, "item added to cart")
    return redirect(reverse('occasion_product'))


#gymming service
@login_required
def gym_product(request):
    object_list = Gym.objects.all()
    filtered_orders = Order_gym.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "myapp/gym_product.html", context)