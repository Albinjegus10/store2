from django.urls import path
from .views import hello, blog, Shop, shop_details, Shopping_cart,CheckoutView, success_page,cusser,sucessuser1
from .views import aboutus, Shop_low, Shop_top, search_cat_view, signup, login_view, logout_view,AddToCart,get_cart_count,update_cart, remove_from_cart
from .views import order_payment,payment_success,my_order_view,download_invoice_view,my_profile_view,sucessuser2,my_wish_view, yourorder, returnorder, cancel_order, return_order, update_profile, Privacy, Contact
from store import views

urlpatterns = [
    path('', hello, name='hello'),
    path('home/', hello, name='home'),

    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),

    path('shop/',Shop, name='shop'),
    path('shop_low/', Shop_low, name='shop_low'),
    path('shop_top/', Shop_top, name='shop_top'),

    path('blog/', blog, name='blog'),



    path('success/', success_page, name='success_page'),
    path('aboutus/', aboutus, name='aboutus'),
    path('customerservice/', cusser.as_view(), name='customerservice'),

    path('search', views.search_view, name='search'),
    path('search_cat/<int:category_id>/', search_cat_view, name='search_cat'),

    path('shop_details/<int:product_id>/', shop_details, name='shop_details'),
    path('shop_details/', shop_details, name='shop_details'),

    path('shopping_cart/', Shopping_cart.as_view(), name='shopping_cart'),
    path('shopping_cart/<int:product_id>/', Shopping_cart.as_view(), name='shopping_cart'),


    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('sucessuser1/', sucessuser1, name='sucessuser1'),
    path('sucessuser2/', sucessuser2, name='sucessuser2'),


    path('add_to_cart/<int:product_id>/', AddToCart, name='add_to_cart'),
    path('get_cart_count/', get_cart_count, name='get_cart_count'),
    path('update_cart/', update_cart, name='update_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),


    path('payment/', order_payment, name='payment'),
    path('payment_success/', payment_success, name='payment_success'),

    path('my-profile/', my_profile_view,name='my-profile'),
    path('my-wish/', my_wish_view,name='my-wish'),

    path('order_history/', my_order_view, name='order_history'),
    path('download-invoice/<int:orderID>/<int:productID>', download_invoice_view,name='download-invoice'),

    # path('chatbot_response/', chatbot_response, name='chatbot_response'),


    path('yourorder/', yourorder, name='yourorder'),
    path('returnorder/', returnorder, name='returnorder'),
    path('customerservice/', cusser.as_view(), name='customerservice'),
    path('cancel_order/<int:product_id>/', cancel_order, name='cancel_order'),
    path('return_order/<int:product_id>/', return_order, name='return_order'),
    path('update_profile/', update_profile, name='update_profile'),
    path('profile/', update_profile, name='profile'),
    path('privacy_policy/', Privacy.as_view(), name='privacy_policy'),

    path('contact/', Contact.as_view(), name='contact'),

]




