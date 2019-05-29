from django.urls import path
from .views import fugeDetailView
from .views import BarcodeDetailView
from . import views


urlpatterns = [
    path('', views.home, name='UI-home'),
    path('Userfridgelist/<int:pk>/', fugeDetailView.as_view(), name='fuge-detail'),
    path('Barcode/<int:pk>/', BarcodeDetailView.as_view(), name='Barcode-detail'),
    path('register/', views.register, name='UI-register'),
    path('order/', views.automated_order, name='UI-order'),
    path('my_orders/', views.my_orders, name='UI-my_orders'),
    path('unregister/', views.unregister, name='UI-unregister'),
    path('wishlist/', views.wishlist, name='UI-wishlist'),
    path('wishlist/Dairy&Eggs/', views.DairyEggs, name='UI-wishlist-DairyEggs'),
    #path(r'wishlist/Dairy&Eggs/$', views.DairyEggs, name='UI-wishlist-DairyEggs'),
    path('wishlist/Meat&Poultry/', views.MeatPoultry, name='UI-wishlist-MeatPoultry'),
    path('wishlist/wishlistAdd/', views.wishlistAdd, name='UI-wishlist-wishlistAdd'),
    path('about/', views.about, name='UI-about'),
]