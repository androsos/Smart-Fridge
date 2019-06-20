from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from .models import Categories
from .models import Barcode
from .models import fuge
from .forms import HomeForm
from .forms import ScheduleForm
from .models import ela
from django.contrib.auth.models import User
from .models import Userproductlist
from .models import Userfridgelist
from .models import Order
from .models import OrderItem
from .models import AutoOrder
from .models import AutoOrderItem
from .models import OrderHistory
from .models import OrderItemHistory
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.mail import send_mail

#import numpy as np
from collections import Counter
#from background_task import background

# Create your views here.

scheduler = BackgroundScheduler()
job = None



'''
def job():
	current_date = datetime.date.today()
	if current_date == datetime.date.today():
		print('ela')

job()'''

@login_required
def my_orders_breadpastry(request):
	current_user = request.user
	#current_userproductlist = Userproductlist.objects.filter(user=current_user).all()
	current_user_orders = Order.objects.filter(user=current_user).all()

	queryset_list = Barcode.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()


	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	prod_barcode = ''
	order_id = ''
	product = request.GET.get("add_to_order")
	if product:
		query_values_list = product.split(" ")
		prod_barcode = query_values_list[0]
		order_id = query_values_list[1]

		product_in_barcode = Barcode.objects.filter(item_id=prod_barcode).first()
		current_order = Order.objects.filter(order_id=order_id).first()
		item_in_order = OrderItem(order=current_order, product=product_in_barcode)
		item_in_order.save()
		now = timezone.localtime(timezone.now())
		Order.objects.filter(order_id=order_id).update(last_modified=now)
		messages.success(request, f'product added to order!')
		return redirect('UI-my_orders_breadpastry')

	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'title':'Bread & Pastry',
		'prod_barcode':prod_barcode,
		'order_id':order_id,
		'orders':current_user_orders,
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return render(request, 'UI/my_orders/Bread&Pastry.html', context)


@login_required
def my_orders_meatpoultry(request):

	current_user = request.user
	current_user_orders = Order.objects.filter(user=current_user).all()
	queryset_list = Barcode.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()

	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	prod_barcode = ''
	order_id = ''
	product = request.GET.get("add_to_order")
	if product:
		query_values_list = product.split(" ")
		prod_barcode = query_values_list[0]
		order_id = query_values_list[1]

		product_in_barcode = Barcode.objects.filter(item_id=prod_barcode).first()
		current_order = Order.objects.filter(order_id=order_id).first()
		item_in_order = OrderItem(order=current_order, product=product_in_barcode)
		item_in_order.save()
		now = timezone.localtime(timezone.now())
		Order.objects.filter(order_id=order_id).update(last_modified=now)
		messages.success(request, f'product added to order!')
		return redirect('UI-my_orders_meatpoultry')

	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'orders':current_user_orders,
		'title':'Meat & Poultry',
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}

	return render(request, 'UI/my_orders/Meat&Poultry.html', context)

@login_required
def my_orders_dairyeggs(request):
	current_user = request.user
	#current_userproductlist = Userproductlist.objects.filter(user=current_user).all()
	current_user_orders = Order.objects.filter(user=current_user).all()

	queryset_list = Barcode.objects.all().order_by('item_id')
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()


	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	prod_barcode = ''
	order_id = ''
	product = request.GET.get("add_to_order")
	if product:
		query_values_list = product.split(" ")
		prod_barcode = query_values_list[0]
		order_id = query_values_list[1]

		product_in_barcode = Barcode.objects.filter(item_id=prod_barcode).first()
		current_order = Order.objects.filter(order_id=order_id).first()
		item_in_order = OrderItem(order=current_order, product=product_in_barcode)
		item_in_order.save()
		now = timezone.localtime(timezone.now())
		Order.objects.filter(order_id=order_id).update(last_modified=now)
		messages.success(request, f'product added to order!')
		return redirect('UI-my_orders_dairyeggs')
	prev_url = request.META.get('HTTP_REFERER')
	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'title':'Dairy & Eggs',
		'prod_barcode':prod_barcode,
		'order_id':order_id,
		'orders':current_user_orders,
		'prev_url':prev_url,
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}

	return render(request, 'UI/my_orders/Dairy&Eggs.html', context)

@login_required
def my_orders_categories(request):
	queryset_list = Barcode.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()

	context = {'queryset_list':queryset_list, 'categories_list':categories_list, 'title':'Product Categories'}
	return render(request, 'UI/my_orders/categories.html', context)

@login_required
def my_orders(request):
	current_user = request.user

	current_user_orders = Order.objects.filter(user=current_user).all()
	current_user_orderitems = OrderItem.objects.all()

	
	q = request.GET.get("send_order")
	if q:
		now = timezone.localtime(timezone.now())

		Order.objects.filter(user=current_user, order_id=q).update(date_sent=now)

		new_order_history = OrderHistory.objects.create(user=current_user, orderType='my_order', date_sent=now)
						
		order_items = OrderItem.objects.filter(order_id=q).all()
		for order_item in order_items:
			for quantity in range(order_item.quantity):
				new_product_history = OrderItemHistory(product=order_item.product, order=new_order_history)
				new_product_history.save()
		messages.success(request, f'order sent succesfully!')
		return redirect('UI-my_orders')


	q = request.GET.get("delete_order")
	if q:
		if current_user_orders.filter(order_id=q).exists():
			current_user_orders.filter(order_id=q).first().delete()
			messages.success(request, f'order deleted!')
			return redirect('UI-my_orders')
		else:
			messages.warning(request, f'an unexpected error has occured, please try again later ')


	q_new_order = request.GET.get("new_order")
	if q_new_order:
		new_order = Order.objects.create(user=current_user, order_num=1)
		messages.success(request, f'order created!')
		return redirect('UI-my_orders')

	q_edit_order = request.GET.get("edit_order")
	if q_edit_order:
		
		return redirect('UI-my_orders_categories')

	q = request.GET.get("increase_quantity")
	if q:
		q_list = q.split(" ")
		orderitem_id = q_list[0]
		order_id = q_list[1]

		if Order.objects.filter(order_id=order_id, user=current_user).exists():
			current_order = Order.objects.filter(order_id=order_id, user=current_user).first()
			if OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).exists():
				item = OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).first()
				OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).update(quantity=item.quantity + 1)
				now = timezone.localtime(timezone.now())
				Order.objects.filter(order_id=order_id).update(last_modified=now)
				return redirect('UI-my_orders')

	q = request.GET.get("decrease_quantity")
	if q:
		q_list = q.split(" ")
		orderitem_id = q_list[0]
		order_id = q_list[1]

		if Order.objects.filter(order_id=order_id, user=current_user).exists():
			current_order = Order.objects.filter(order_id=order_id, user=current_user).first()
			if OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).exists():
				item = OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).first()
				OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).update(quantity=item.quantity - 1)
				now = timezone.localtime(timezone.now())
				Order.objects.filter(order_id=order_id).update(last_modified=now)
				return redirect('UI-my_orders')

	q = request.GET.get("remove_product_from_order")
	if q:
		q_list = q.split(" ")
		orderitem_id = q_list[0]
		order_id = q_list[1]

		if Order.objects.filter(order_id=order_id, user=current_user):
			current_order = Order.objects.filter(order_id=order_id, user=current_user).first()
			
			if OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order):
				current_orderitem = OrderItem.objects.filter(order_item_id=orderitem_id, order=current_order).first()

				current_orderitem.delete()

				now = timezone.localtime(timezone.now())
				Order.objects.filter(order_id=order_id).update(last_modified=now)

				messages.success(request, f'product removed from order!')
				return redirect('UI-my_orders')
			else:
				messages.warning(request, f'product does not exist !')
		else:
			messages.warning(request, f'order does not exist !')

	paginator = Paginator(current_user_orders, 4)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
		
	context = {
		#'queryset_list':order_items,
		'orders':queryset,
		'orderitems':current_user_orderitems,
		'title':'My Orders'
	}
	return  render(request, 'UI/my_orders.html', context)


def tick():
	all_users = User.objects.all()
	for user in all_users:

		now = timezone.localtime(timezone.now())
		current_day = now.strftime('%A')
		current_time = now.strftime('%H')

		current_date = now.strftime('%d/%m/%Y')

		user_order = AutoOrder.objects.filter(user=user).first()

		if user_order.scheduled_date is not None and user_order.scheduled_time is not None:

			if user_order.scheduled_date == current_day and user_order.scheduled_time == current_time:
				
				if user_order.status != 'cancelled' and timezone.localtime(user_order.date_sent).strftime('%d/%m/%Y') != current_date and user_order.status != "ready":
				
					AutoOrder.objects.filter(user=user).update(status='ready')


def start_job():
	global job
	job = scheduler.add_job(tick, 'interval', seconds=10)
	try:
		scheduler.start()
	except:
		pass


start_job()

def get_current_users():
	active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
	user_id_list = []
	for session in active_sessions:
		data = session.get_decoded()
		user_id_list.append(data.get('_auth_user_id', None))
	return User.objects.filter(id__in=user_id_list)

@login_required
def my_orders_history(request):
	current_user = request.user

	current_user_orders = OrderHistory.objects.filter(user=current_user, orderType='my_order').all()
	current_user_orderitems = OrderItemHistory.objects.all()

	q = request.GET.get("clear_order")
	if q:
		if current_user_orders.filter(order_id=q).exists():
			current_user_orders.filter(order_id=q).first().delete()
			messages.success(request, f'order deleted from your history!')
			return redirect('UI-my_ordersHistory')
		else:
			messages.warning(request, f'an unexpected error has occured, please try again later ')

	q = request.GET.get("add_all")
	if q:
		current_user_order = OrderHistory.objects.filter(order_id=q).first()
		current_order_items = OrderItemHistory.objects.filter(order=current_user_order).all()
		for order_item in current_order_items:
			product_in_barcode = Barcode.objects.filter(item_id=order_item.product.item_id).first()
			product_for_fridge = Userfridgelist(user=current_user, barcode=product_in_barcode)
			product_for_fridge.save()
		messages.success(request, f'products succesfully added to your fridge!')
		return redirect('UI-my_ordersHistory')

	paginator = Paginator(current_user_orders, 4)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True

	context = {
		'orders':queryset,
		'orderitems':current_user_orderitems,
		'title':'My Orders History'
	}
	return  render(request, 'UI/my_orders_history.html', context)

@login_required
def automated_order_history(request):
	current_user = request.user

	current_user_orders = OrderHistory.objects.filter(user=current_user, orderType='auto').all()
	current_user_orderitems = OrderItemHistory.objects.all()

	q = request.GET.get("clear_order")
	if q:
		if current_user_orders.filter(order_id=q).exists():
			current_user_orders.filter(order_id=q).first().delete()
			messages.success(request, f'order deleted from your history!')
			return redirect('UI-scheduledHistory')
		else:
			messages.warning(request, f'an unexpected error has occured, please try again later ')

	q = request.GET.get("add_all")
	if q:
		current_user_order = OrderHistory.objects.filter(order_id=q).first()
		current_order_items = OrderItemHistory.objects.filter(order=current_user_order).all()
		for order_item in current_order_items:
			product_in_barcode = Barcode.objects.filter(item_id=order_item.product.item_id).first()
			product_for_fridge = Userfridgelist(user=current_user, barcode=product_in_barcode)
			product_for_fridge.save()
		messages.success(request, f'products succesfully added to your fridge!')
		return redirect('UI-scheduledHistory')

	paginator = Paginator(current_user_orders, 4)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True

	context = {
		'orders':queryset,
		'orderitems':current_user_orderitems,
		'title':'Scheduled Orders History'
	}
	return  render(request, 'UI/scheduled_history.html', context)

@login_required
def automated_order(request):
	current_user = request.user

	queryset_list = get_current_users().all()
	
	current_user_order = AutoOrder.objects.filter(user=current_user).first()
	current_user_orders = AutoOrder.objects.filter(user=current_user).all()

	current_user_orderitems = AutoOrderItem.objects.filter(order=current_user_order).all()

	
	if request.method == 'POST':
		form = ScheduleForm(request.POST)
		if form.is_valid():
			desired_day = form.cleaned_data.get('scheduled_day')
			desired_time = form.cleaned_data.get('scheduled_time')
			AutoOrder.objects.filter(user=current_user).update(scheduled_date=desired_day)
			AutoOrder.objects.filter(user=current_user).update(scheduled_time=desired_time)
			AutoOrder.objects.filter(user=current_user).update(status="scheduled")
			messages.success(request, f'Order scheduled date updated succesfully !')
			return redirect('UI-order')
	else:
		form = ScheduleForm()

	q = request.GET.get("confirm_order")
	if q:
		now = timezone.localtime(timezone.now())

		user_order = AutoOrder.objects.filter(user=current_user, auto_order_id=q).first()

		AutoOrder.objects.filter(user=current_user, auto_order_id=q).update(status='sent')
		AutoOrder.objects.filter(user=current_user, auto_order_id=q).update(date_sent=now)

		#add to history
		new_order_history = OrderHistory.objects.create(user=current_user, orderType='auto', date_sent=now)
					
		auto_order_items = AutoOrderItem.objects.filter(order=user_order).all()
		for auto_order_item in auto_order_items:
			new_product_history = OrderItemHistory(product=auto_order_item.product, order=new_order_history)
			new_product_history.save()
		messages.success(request, f'Order sent succesfully! You can view your sent orders in the orders history.')
		return redirect('UI-order')

	q = request.GET.get("cancel_order")
	if q:
		AutoOrder.objects.filter(user=current_user, auto_order_id=q).update(status="cancelled")
		messages.success(request, f'Order cancelled !')
		return redirect('UI-order')

	q = request.GET.get("update_order")
	if q:
		for auto_order_item in current_user_orderitems:
			auto_order_item.delete()

		current_user_productlist = Userproductlist.objects.filter(user=current_user).values_list('product')
		current_user_fridgelist = Userfridgelist.objects.filter(user=current_user).values_list('barcode')

		c1 = Counter(current_user_productlist)
		c2 = Counter(current_user_fridgelist)

		diff = c1-c2
		res = list(diff.elements())
		items_list = [item for t in res for item in t] 

		current_user_order = AutoOrder.objects.filter(user=current_user, auto_order_id=q).first()
		for product in items_list:
			product_in_barcode = Barcode.objects.filter(id=product).first()
			product_for_order = AutoOrderItem(order=current_user_order, product=product_in_barcode)
			product_for_order.save()

		return redirect('UI-order')

	
	if current_user_order.status == 'ready':
		messages.info(request, f'scheduled order ready !')
	
	order_items = AutoOrderItem.objects.filter(order=current_user_order).all()

	context = {
		'queryset_list':queryset_list,
		'orders':current_user_orders,
		'orderitems':current_user_orderitems,
		'form':form,
		'title':'Scheduled Order'
	}
	return  render(request, 'UI/order.html', context)

class fugeDetailView(LoginRequiredMixin, DetailView):
	model = Userfridgelist
	#template name <app>/<model>_<viewtype>.html

class BarcodeDetailView(LoginRequiredMixin, DetailView):
	model = Barcode
	
	#template name <app>/<model>_<viewtype>.html
	def get_context_data(self, **kwargs):
		context = super(BarcodeDetailView, self).get_context_data(**kwargs)
		context['prev_url'] = self.request.META.get('HTTP_REFERER')
		context['title'] = 'Product Details'
		return context		

@login_required
def register(request): 
	current_user = request.user

	if request.method == 'POST':
		form = HomeForm(request.POST)
		if form.is_valid():
			barcode = form.cleaned_data.get('barcode')
			if Barcode.objects.filter(item_id=barcode).exists():
				bar_product = Barcode.objects.filter(item_id=barcode).first()
				new_product = Userfridgelist(barcode=bar_product, user=current_user)
				new_product.save()
				messages.success(request, f'product with barcode {barcode} inserted !')
			else:
				messages.warning(request, f'product with barcode {barcode} does not exist !')
			return redirect('UI-register')
	else:
		form = HomeForm()
	

	context = {'form':form, 'title':'Add To Fridge'}
	return  render(request, 'UI/register.html', context)

@login_required
def unregister(request):

	current_user = request.user
	current_userfridgelist = Userfridgelist.objects.filter(user=current_user).all()

	if request.method == 'POST':
		form = HomeForm(request.POST)
		if form.is_valid():
			barcode = form.cleaned_data.get('barcode')
			if Barcode.objects.filter(item_id=barcode).exists():
				bar_product = Barcode.objects.filter(item_id=barcode).last()
				current_userfridgelist.filter(barcode=bar_product).first().delete()
				messages.success(request, f'product with barcode removed {barcode}!')
			else:
				messages.warning(request, f'product with barcode {barcode} does not exist !')
			return redirect('UI-unregister')
	else:
		form = HomeForm()
	

	context = {'form':form, 'title':'Remove From Fridge'}
	return  render(request, 'UI/unregister.html', context)


@login_required
def home(request):
	current_user = request.user

	current_userfridgelist = Userfridgelist.objects.filter(user=current_user).all()
	queryset_list = current_userfridgelist.all().order_by("-insert_date")

	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True

	product = request.GET.get("remove_product")
	if product:
		if current_userfridgelist.filter(item_id=product).exists():
			current_userfridgelist.filter(item_id=product).first().delete()
			messages.success(request, f'product deleted!')
			return redirect('UI-home')
		else:
			messages.warning(request, f'an unexpected error has occured, please try again later ')

	curr_date = timezone.localtime(timezone.now())

	context = {
		'categories': Categories.objects.all(), 
		'title':'Home',
		'curr_date':curr_date,
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return  render(request, 'UI/home.html',  context)

def about(request):
	return  render(request, 'UI/about.html', {'title': 'about'})

@login_required
def wishlist(request):
	#queryset_list = ela.objects.all()
	current_user = request.user
	current_userproductlist = Userproductlist.objects.filter(user=current_user).all()
	queryset_list = current_userproductlist.all()


	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	product = request.GET.get("remove_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		if current_userproductlist.filter(product=product_in_barcode).exists():
			current_userproductlist.filter(product=product_in_barcode).first().delete()
			messages.success(request, f'product removed!')
			return redirect('UI-wishlist')
		else:
			messages.warning(request, f'an unexpected error has occured !')

	context = {
		#'queryset_list':queryset_list, 
		'title':'Wishlist', 
		'wishlist':current_userproductlist, 
		'current_user':current_user,
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return render(request, 'UI/wishlist/wishlist.html', context)


	
@login_required
def wishlistAdd(request):

	queryset_list = Barcode.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()

	context = {'queryset_list':queryset_list, 'categories_list':categories_list, 'title':'Product Categories'}
	return render(request, 'UI/wishlist/wishlistAdd.html', context)

@login_required
def DairyEggs(request):

	current_user = request.user
	#current_userproductlist = Userproductlist.objects.filter(user=current_user).all()
	current_user_orders = Order.objects.filter(user=current_user).all()

	queryset_list = Barcode.objects.all().order_by('item_id')
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()


	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	product = request.GET.get("add_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		product_in_wishlist = Userproductlist(product=product_in_barcode, user=current_user)
		product_in_wishlist.save()
		messages.success(request, f'product added!')
		return redirect('UI-wishlist-DairyEggs')

	product = request.GET.get("remove_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		if ela.objects.filter(product=product_in_barcode).exists():
			ela.objects.filter(product=product_in_barcode).first().delete()
			return redirect('UI-wishlist-DairyEggs')

	prod_barcode = ''
	order_id = ''
	product = request.GET.get("add_to_order")
	if product:
		query_values_list = product.split(" ")
		prod_barcode = query_values_list[0]
		order_id = query_values_list[1]

		product_in_barcode = Barcode.objects.filter(item_id=prod_barcode).first()
		
		current_order = Order.objects.filter(order_id=order_id).first()
		item_in_order = OrderItem(order=current_order, product=product_in_barcode)
		item_in_order.save()
		now = timezone.localtime(timezone.now())
		Order.objects.filter(order_id=order_id).update(last_modified=now)
		messages.success(request, f'product added to order!')
		return redirect('UI-wishlist-DairyEggs')
	prev_url = request.META.get('HTTP_REFERER')
	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'title':'Dairy & Eggs',
		'prod_barcode':prod_barcode,
		'order_id':order_id,
		'orders':current_user_orders,
		'prev_url':prev_url,
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return render(request, 'UI/wishlist/Dairy&Eggs.html', context)
	

@login_required
def MeatPoultry(request):

	current_user = request.user
	current_user_orders = Order.objects.filter(user=current_user).all()
	queryset_list = Barcode.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()

	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	product = request.GET.get("add_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		product_in_wishlist = Userproductlist(product=product_in_barcode, user=current_user)
		product_in_wishlist.save()
		messages.success(request, f'product added!')
		return redirect('UI-wishlist-MeatPoultry')

	product = request.GET.get("remove_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		if ela.objects.filter(product=product_in_barcode).exists():
			ela.objects.filter(product=product_in_barcode).first().delete()
			return redirect('UI-wishlist-MeatPoultry')

	prod_barcode = ''
	order_id = ''
	product = request.GET.get("add_to_order")
	if product:
		query_values_list = product.split(" ")
		prod_barcode = query_values_list[0]
		order_id = query_values_list[1]

		product_in_barcode = Barcode.objects.filter(item_id=prod_barcode).first()
		current_order = Order.objects.filter(order_id=order_id).first()
		item_in_order = OrderItem(order=current_order, product=product_in_barcode)
		item_in_order.save()
		now = timezone.localtime(timezone.now())
		Order.objects.filter(order_id=order_id).update(last_modified=now)
		messages.success(request, f'product added to order!')
		return redirect('UI-wishlist-MeatPoultry')

	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'orders':current_user_orders,
		'title':'Meat & Poultry',
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return render(request, 'UI/wishlist/Meat&Poultry.html', context)

@login_required
def BreadPastry(request):

	current_user = request.user
	#current_userproductlist = Userproductlist.objects.filter(user=current_user).all()
	current_user_orders = Order.objects.filter(user=current_user).all()

	queryset_list = Barcode.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(name__icontains=query)

	categories_list =  Categories.objects.all()


	paginator = Paginator(queryset_list, 12)

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		#if page not an integer, deliver first page
		queryset = paginator.page(1)
	except EmptyPage:
		#if page is out of rage, deliver last page of results
		queryset = paginator.page(paginator.num_pages)
	is_paginated = True
	#queryset_list = Userfridgelist.objects.all()

	product = request.GET.get("add_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		product_in_wishlist = Userproductlist(product=product_in_barcode, user=current_user)
		product_in_wishlist.save()
		messages.success(request, f'product added!')
		return redirect('UI-BreadPastry')

	product = request.GET.get("remove_product")
	if product:
		product_in_barcode = Barcode.objects.filter(item_id=product).first()
		if ela.objects.filter(product=product_in_barcode).exists():
			ela.objects.filter(product=product_in_barcode).first().delete()
			return redirect('UI-BreadPastry')

	prod_barcode = ''
	order_id = ''
	product = request.GET.get("add_to_order")
	if product:
		query_values_list = product.split(" ")
		prod_barcode = query_values_list[0]
		order_id = query_values_list[1]

		product_in_barcode = Barcode.objects.filter(item_id=prod_barcode).first()
		current_order = Order.objects.filter(order_id=order_id).first()
		item_in_order = OrderItem(order=current_order, product=product_in_barcode)
		item_in_order.save()
		now = timezone.localtime(timezone.now())
		Order.objects.filter(order_id=order_id).update(last_modified=now)
		messages.success(request, f'product added to order!')
		return redirect('UI-BreadPastry')

	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'title':'Bread & Pastry',
		'prod_barcode':prod_barcode,
		'order_id':order_id,
		'orders':current_user_orders,
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return render(request, 'UI/Bread&Pastry.html', context)