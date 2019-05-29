from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from .models import Categories
from .models import Barcode
from .models import fuge
from .forms import HomeForm
from .models import ela
from django.contrib.auth.models import User
from .models import Userproductlist
from .models import Userfridgelist
from .models import Order
from .models import OrderItem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
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
def my_orders(request):
	current_user = request.user

	current_user_orders = Order.objects.filter(user=current_user).all()
	current_user_orderitems = OrderItem.objects.all()

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
				messages.success(request, f'product removed from order!')
				return redirect('UI-my_orders')
			else:
				messages.warning(request, f'product does not exist !')
		else:
			messages.warning(request, f'order does not exist !')


		
	context = {
		#'queryset_list':order_items,
		'orders':current_user_orders,
		'orderitems':current_user_orderitems,
		'title':'My Orders'
	}
	return  render(request, 'UI/my_orders.html', context)

'''
def tick():
		print('One tick!')

def start_job():
	global job
	job = scheduler.add_job(tick, 'interval', seconds=2)
	try:
		scheduler.start()
	except:
		pass


start_job()
'''
from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour=10, minute=4, day_of_week="wed"))
def every_monday_morning():
	print("This is run every Monday morning at 7:30")

every_monday_morning()

@login_required
def automated_order(request):
	current_user = request.user


	

	


	#sugkrish wishlist me fridgelist

	'''
	current_user_productlist = Userproductlist.objects.filter(user=current_user).values_list('product')
	current_user_fridgelist = Userfridgelist.objects.filter(user=current_user).values_list('barcode')
	product_missing_num = len(set(current_user_productlist).difference(set(current_user_fridgelist)))

	current_user_productlist = Userproductlist.objects.filter(user=current_user).all()
	current_user_fridgelist = Userfridgelist.objects.filter(user=current_user).all()

	
	count = 0
	for product_in_productlist in current_user_productlist:
		exists = False
		for product_in_fridgelist in current_user_fridgelist:
			if product_in_productlist.product == product_in_fridgelist.barcode:
				exists = True
		if exists == False:
			count = count+1

	if(count >= 4):
		new_order = Order.objects.create(user=current_user, order_num=1)
		for product_in_productlist in current_user_productlist:
			exists = False
			for product_in_fridgelist in current_user_fridgelist:
				if product_in_productlist.product == product_in_fridgelist.barcode:
					exists = True
			if exists == False:
				#product_in_productlist.product exists in productlist but not in fridgelist
				product_for_order = OrderItem(order=new_order, product=product_in_productlist.product, quantity=1)
				product_for_order.save()
		order_items = OrderItem.objects.filter(order=new_order).all()
	'''
	context = {
		#'queryset_list':order_items,
		#'count':count
	}
	return  render(request, 'UI/order.html', context)

class fugeDetailView(LoginRequiredMixin, DetailView):
	#model = fuge
	model = Userfridgelist
	#template name <app>/<model>_<viewtype>.html

class BarcodeDetailView(LoginRequiredMixin, DetailView):
	#model = fuge
	model = Barcode
	#template name <app>/<model>_<viewtype>.html		

@login_required
def register(request): #bazei products ston pinaka fuge, pou einai o infridge

	current_user = request.user

	if request.method == 'POST':
		form = HomeForm(request.POST)
		if form.is_valid():
			barcode = form.cleaned_data.get('barcode')
			if Barcode.objects.filter(item_id=barcode).exists():
				bar_product = Barcode.objects.filter(item_id=barcode).first()
				new_product = Userfridgelist(barcode=bar_product, user=current_user)
				new_product.save()
				messages.success(request, f'barcode {barcode} inserted !')
			else:
				messages.warning(request, f'barcode {barcode} does not exist !')
			return redirect('UI-register')
	else:
		form = HomeForm()
	

	context = {'form':form, 'title':'Register'}
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
				messages.success(request, f'barcode removed {barcode}!')
			else:
				messages.warning(request, f'barcode {barcode} does not exist !')
			return redirect('UI-unregister')
	else:
		form = HomeForm()
	

	context = {'form':form, 'title':'Unregister'}
	return  render(request, 'UI/unregister.html', context)

@login_required
def home(request):
	#entry_obj = Barcode.objects.filter(item_id=barcode).exists()

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
	#queryset_list = Userfridgelist.objects.all()

	product = request.GET.get("remove_product")
	if product:
		#product_in_barcode = Barcode.objects.filter(id=product).first()
		#if fuge.objects.filter(barcode=product_in_barcode).exists():
		#	fuge.objects.filter(barcode=product_in_barcode).first().delete()
		if current_userfridgelist.filter(item_id=product).exists():
			current_userfridgelist.filter(item_id=product).first().delete()
			messages.success(request, f'product deleted!')
			return redirect('UI-home')
		else:
			messages.warning(request, f'an unexpected error has occured, please try again later ')

	context = {
		#'posts': posts
		'categories': Categories.objects.all(), #pairnoyme ta data apo thn database ki oxi apo panw
		'title':'Home',
		#'queryset_list':queryset_list
		'queryset_list':queryset,
		'is_paginated':is_paginated
	}
	return  render(request, 'UI/home.html', context)

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
		messages.success(request, f'product added to order!')
		return redirect('UI-wishlist-DairyEggs')

	context = {
		#'queryset_list':queryset_list, 
		'categories_list':categories_list, 
		'title':'Dairy & Eggs',
		'prod_barcode':prod_barcode,
		'order_id':order_id,
		'orders':current_user_orders,
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
