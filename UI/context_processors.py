from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Userfridgelist
from .models import AutoOrder
from django.utils import timezone


def home_notification(request):

	notify_danger = False
	notify_warning = False
	if request.user.is_authenticated:

		current_user = request.user

		products_in_fridge = Userfridgelist.objects.filter(user=current_user).all()
		
		for product in products_in_fridge:
			delta = timezone.localtime(timezone.now()) - timezone.localtime(product.insert_date)
			date_diff = int(delta.days)
			if date_diff == 3:
				notify_warning = True
			if date_diff > 3:
				notify_danger = True

	
	return {'notify_danger': notify_danger, 'notify_warning': notify_warning}

def order_notification(request):

	ready_order = False
	if request.user.is_authenticated:

		current_user = request.user

		user_order = AutoOrder.objects.filter(user=current_user).first()
		if user_order.status == "ready":
			ready_order = True
		else:
			ready_order = False

	return {'ready_order': ready_order}