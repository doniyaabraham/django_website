"""
URL configuration for wedding project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    #login,sigin,main
    path('index', views.index),
    path('logout',views.logout),
    path('',views.new),
    path('login', views.login),
    path('register', views.register),
    path('edit', views.edit),
    path('thanku', views.thanku),
    path("forgot",views.forgot_password,name="forgot"),
    path("reset/<token>", views.reset_password, name="reset"),
    path("reset/reset2/<token>", views.reset_password2, name="reset2"),


    path('reply/<em>',views.reply,name='reply'),
    path('reply/replymail/<em>',views.replymail,name='replymail'),
    path('booking_dtls', views.booking_dtls),
    # path('payments/<int:d>', views.payments),
    #to buy items
    path('checkout', views.checkout, name="checkout"),
    path('place-order', views.placeorder, name='placeorder'),
    path('proceed-to-pay', views.razorpaycheck, name='proceed-to-pay'),
    path('proceed-to-pay1', views.razorpaycheck1, name='proceed-to-pay1'),
    path('myorder', views.orderss, name='myorder'),
    #add items,remove etc
    path('removewish/<int:d>', views.removewish),
    path('removeorder/<int:d>', views.removeorder
         ),
    path('remove/<int:d>', views.remove),
    path('cart/increment/<int:cart_id>/', views.increment_quantity, name='increment_quantity'),
    path('cart/decrement/<int:cart_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('cart_details', views.cart_details),
    path('addcart/<int:d>', views.addcart),
    path('addcarti/<int:d>', views.addcarti),
    path('addcart2/<int:d>', views.addcart2),
    path('addimage/<int:d>', views.addimage),
    path('buynowsi/<int:prod_id>/', views.buynowsi, name='buynowsi'),
    path('buynows', views.buycart),
    path('buynow/increment/<int:cart_id>/', views.increment_quantity1, name='increment_quantity1'),
    path('buynow/decrement/<int:cart_id>/', views.decrement_quantity1, name='decrement_quantity1'),
    path('removeb/<int:d>', views.removeb),
    path('checkoutbuynow', views.checkoutbuynow, name="checkoutbuynow"),
    path('place-orderbuynow', views.placeorderbuynow, name='placeorderbuynow'),
    path('wish', views.wish),
    path('search', views.search),
    path('wishcart/<int:d>', views.wishcart),
    path('wishcart2/<int:d>', views.wishcart2),
    path('shotr', views.shotr),
    path('view-product/', views.view_product, name='view_product'),
    path('user-order-track/<int:pid>/', views.user_order_track, name="user_order_track"),
    path('change-order-status/<int:pid>/', views.change_order_status, name="change_order_status"),
    #adminside
    path('adminside',views.adminside),
    path('update/<int:d>', views.update),
    path('update1/<int:d>', views.update1),
    path('delete/<int:d>', views.delete),
    path('delete1/<int:d>', views.delete1),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

