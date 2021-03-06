from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


class Categories(models.Model):
	category_id = models.IntegerField(primary_key=True)
	category_name = models.TextField(max_length=100)
	image = models.ImageField(upload_to='category_image', blank='True')

	#def __str__(self):
	#	return str(self.category_id)

	def __str__(self):
		return "%s %s" % (str(self.category_id), self.category_name)


class Barcode(models.Model):
	item_id = models.IntegerField() #to barcode number
	name = models.TextField(max_length=100) #to full name tou proiontos
	category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING)
	product_name = models.TextField(max_length=100, default='unknown')
	brand_name = models.TextField(max_length=100, default='unknown')
	measure_type = models.TextField(max_length=100, default='unknown')
	quantity = models.IntegerField(default=0)
	image = models.ImageField(upload_to='barcode_image', blank='True')

	def __str__(self):
		return "%s %s %s %s %s" % (str(self.item_id), self.product_name, 
			self.brand_name, str(self.quantity), self.measure_type)

class ela(models.Model): #WISHLIST
	item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	#user = models.OneToOneField(User, on_delete=models.CASCADE) #an diagrafei o user, diagrafetai o ela
	product = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING, default='')

class fuge(models.Model): #INFRIDGE
	item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	#user = models.OneToOneField(User, on_delete=models.CASCADE) #an diagrafei o user, diagrafetai o fuge
	barcode = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING, default='')
	insert_date = models.DateTimeField(default=timezone.now)
	#user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default='')

	def __str__(self):
		return "%s %s %s %s %s %s" % (str(self.barcode.item_id), self.barcode.product_name, 
			self.barcode.brand_name, str(self.barcode.quantity), self.barcode.measure_type, 
			str(self.insert_date))

	def get_absolute_url(self):
		return reverse('fuge-detail', kwargs={'pk':self.pk})




class Userproductlist(models.Model): #WISHLIST
	item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default='') 
	product = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING, blank=True, null=True)

	def __str__(self):
		return f'{self.user.username} Product List'


class Userfridgelist(models.Model): #INFRIDGE
	item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default='') 
	barcode = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING, blank=True, null=True)
	insert_date = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return "%s %s %s %s %s %s" % (str(self.barcode.item_id), self.barcode.product_name, 
			self.barcode.brand_name, str(self.barcode.quantity), self.barcode.measure_type, 
			str(self.insert_date))

class Order(models.Model):
	order_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default='') #an diagrafei o user, diagrafetai to order
	order_num = models.IntegerField()
	date_sent = models.DateTimeField(null=True)
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True, null=True)

class OrderItem(models.Model):
	order_item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True) #an diagrafei to order, diagrafete kai to orderItem object
	product = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING)
	quantity = models.IntegerField(default=1)
	desc = models.TextField(max_length=500, null=True, blank=True)
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

class AutoOrder(models.Model):
	auto_order_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.TextField(max_length=20, default='not_init')
	scheduled_date = models.TextField(null=True)
	scheduled_time = models.TextField(null=True)
	date_sent = models.DateTimeField(null=True)
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
		
class AutoOrderItem(models.Model):
	order_item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	order = models.ForeignKey(AutoOrder, on_delete=models.CASCADE, null=True)	
	product = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING)
	last_modified = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

class OrderHistory(models.Model):
	order_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
	orderType = models.TextField(max_length=20, default='unknown')
	date_sent = models.DateTimeField()

class OrderItemHistory(models.Model):
	order_item_id = models.AutoField(primary_key=True, serialize=False, verbose_name='ID')
	product = models.ForeignKey(Barcode, on_delete=models.DO_NOTHING)
	order = models.ForeignKey(OrderHistory, on_delete=models.CASCADE, null=True)