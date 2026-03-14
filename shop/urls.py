from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('products/', views.products, name='products'),
    path('add-to-cart/<int:pid>/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart, name='cart'),

    path('increase/<int:pid>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:pid>/', views.decrease_qty, name='decrease_qty'),
    path('remove/<int:pid>/', views.remove_item, name='remove_item'),
    path('payment/', views.payment, name='payment'),

    path('buy/', views.pay, name='pay'),
    path('orders/', views.order_history, name='orders'),
    path('rate/<int:pid>/', views.add_rating, name='add_rating'),  

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

]