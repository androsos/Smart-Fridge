from django.contrib import admin
from .models import Categories
from .models import Barcode
#from .models import InFridgeItem
#from .models import WishlistItem
from .models import ela
from .models import fuge

from .models import Userproductlist
from .models import Userfridgelist

from .models import Order
from .models import OrderItem

from .models import AutoOrder
from .models import AutoOrderItem

from .models import OrderHistory
from .models import OrderItemHistory

# Register your models here.

admin.site.register(Categories)
admin.site.register(Barcode)

#admin.site.register(InFridgeItem)
#admin.site.register(WishlistItem)

#admin.site.register(ela)
#admin.site.register(fuge)

admin.site.register(Userproductlist)
admin.site.register(Userfridgelist)

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(AutoOrder)
admin.site.register(AutoOrderItem)

admin.site.register(OrderHistory)
admin.site.register(OrderItemHistory)