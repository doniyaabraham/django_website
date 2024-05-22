
# Create your views here.


from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.http import JsonResponse

from .models import*
from django.db import connection
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
import datetime
import razorpay
from django.contrib import messages
from django.conf import settings
import re
import random
def index(r):#sub index
   if 'id' in r.session:
       if r.method == 'POST':
           name = r.POST['name']
           email = r.POST['email']
           messg = r.POST['mssg']
           data = feedback.objects.create(name=name, email=email, messg=messg)

           data.save()
           messages.success(r, 'Data saved')
       product=products.objects.all()
       user=userdetails.objects.all()
       user = userdetails.objects.get(username=r.session['id'])
       count_item = cart.objects.filter(user_details=user).values_list('product_details_id', flat=True)
       count_items = cart.objects.filter(user_details=user).count()
       print(count_items)
       out_of_stock_products = products.objects.filter(stock=0)
       user2 = userdetails.objects.get(username=r.session['id'])
       wish_item = wishlist.objects.filter(user_details=user2).values_list('product_details_id', flat=True)
       wish_items = wishlist.objects.filter(user_details=user2).count()
       print(wish_items)
       return render(r,'index.html',{'product':product,'user':user,'count_items': count_items,'count_item': count_item,'wish_items': wish_items,'wish_item': wish_item,'out_of_stock_products': out_of_stock_products})
   else:
       return redirect(login)
def new(r):#the opeing page

        if r.method == 'POST':
            name = r.POST['name']
            email = r.POST['email']
            messg = r.POST['mssg']
            data = feedback.objects.create(name=name, email=email, messg=messg)

            data.save()
            messages.success(r, 'Data saved')
        return render(r,'new.html')



def logout(r):
  if 'id' in r.session or 'id1' in r.session:
      r.session.flush()
      return redirect(login)
  return  redirect(login)
def edit(r):
    if r.method =='POST':
        print("**************")
        firstname = r.POST['firstname']
        lastname = r.POST['lastname']
        email = r.POST['email']
        phno = r.POST['phno']
        address=r.POST['address']
        password = r.POST['password']
        username = r.POST['username']
        userdetails.objects.filter(firstname=firstname).update( email=email,lastname=lastname,address=address, phno=phno, password=password,username=username)
        messages.success(r, 'updated')
    if 'id' in r.session:
        data = userdetails.objects.get(username=r.session['id'])
        return render(r, 'edit.html', {'data': data})

    else:
        # Handle the case where 'id' is not present in the session
        return HttpResponse("User id not found in session.")


def login(r):
    if r.method == 'POST':

        u = r.POST['username']
        p = r.POST['password']

        try:
            data = userdetails.objects.get(username=u)
            print(data, data.password)
            if data.password == p:
                r.session['id'] = u
                return redirect(index)

            else:

                messages.error(r, 'incorrect password')
        except:
            if u == 'admin' and p == 'adminpassword':
                r.session['id1'] = u
                return redirect(adminside)
            else:

                messages.error(r, 'User not found')
    return render(r, 'login.html')

def register(r):
    if r.method == 'POST':
        firstname = r.POST['firstname']
        lastname = r.POST['lastname']
        email = r.POST['email']
        address=r.POST['address']
        username = r.POST['username']
        password = r.POST['password']
        phno = r.POST['phno']
        pwd = r.POST['conpassword']
        if password == pwd:
            if userdetails.objects.filter(username=username).exists():
                messages.info(r, "Username already exists")
                return redirect(register)
            elif userdetails.objects.filter(email=email).exists():
                messages.info(r, "Email already exists")
                return redirect(register)
            else:
                try:
                    y = re.search("(?=.{8,})(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[~!@#$%^&*?])",password)
                    x = re.findall(r'^[0-9]{10}',phno)

                    if x == [phno]:
                        if y == None:
                            messages.info(r, "Password is not strong", extra_tags="signup")
                            return redirect(register)
                        else:
                            val = userdetails.objects.create(firstname=firstname, address=address,lastname=lastname,email=email, password=password, username=username, phno=phno)
                            val.save()
                            return redirect(login)
                    else:
                        messages.info(r, "Not a valid phone number", extra_tags="signup")
                        return redirect(register)
                except:
                    messages.info(r, "Invalid input", extra_tags="signup")
        else:
            messages.info(r, "Password doesn't match", extra_tags="signup")
            return redirect(register)

    return render(r, 'register.html')


def search(r):
 if 'id' in r.session:
    if r.method =='POST':
        print("**************")
        prod_name = r.POST['product_name']
        print(prod_name)
        data = products.objects.filter(product_name=prod_name)
        user = userdetails.objects.get(username=r.session['id'])
        user2 = userdetails.objects.get(username=r.session['id'])
        count_item = cart.objects.filter(user_details=user).values_list('product_details_id', flat=True)
        wish_item = wishlist.objects.filter(user_details=user2).values_list('product_details_id', flat=True)
        print(data)
        if data:
          return render(r,'search.html',{'data':data,'count_item':count_item,'wish_item':wish_item })
        else:
            messages.success(r, 'Item is not found')
    return render(r, 'search.html')
 return redirect(login)

def thanku(r):
    return render(r, 'thanku.html', )

def shotr(r):
    return render(r, 'product-details.html', )

def removeorder(r, d):
        order_item = order.objects.get(pk=d)
        order_item.delete()
        return redirect(orderss)
def orderss(r):
    if 'id' in r.session:

        user = userdetails.objects.get(username=r.session['id'])
        c = cart.objects.filter(user_details=user.id).all()
        o = order.objects.all()
        l=[]
        for i in o:
            if i.user==user:
                l.append(i)
        return render(r,'myorders.html',{'l':l})
    return render(r,'myorders.html')

def user_order_track(request, pid):
    orders = order.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "user-order-track.html", locals())
def change_order_status(request, pid):
    orders = order.objects.get(id=pid)
    status = request.GET.get('statuss')
    if status:
        orders.statuss = status
        orders.save()
        messages.success(request, "Order status changed.")
    return redirect(orderss)
#cart functions start
#

def placeorder(r):#main checkout
    if 'id' in r.session:
        user = userdetails.objects.get(username=r.session['id'])
        c = cart.objects.filter(user_details=user.id).all()

        t = 0
        for i in c:
            item = products.objects.get(pk=i.product_details.pk)
            t = t + (i.product_details.price * i.quantity)

        if r.method == 'POST':
            if r.POST.get('save') == 'save':
                # Validation and saving profile details
                # Code for validating and saving profile details...
                # This part remains unchanged
                fname = r.POST.get('fname')
                lname = r.POST.get('lname')
                email = r.POST.get('email')
                phone = r.POST.get('phone')
                address = r.POST.get('address')
                city = r.POST.get('city')
                state = r.POST.get('state')
                country = r.POST.get('country')
                pincode = r.POST.get('pincode')
                # phone_regex = r'^[6-9][0-9]{9}$'
                # pincode_regex = r'^[1-9][0-9]{5}$'
                #
                # Validating phone number
                # if not re.match(phone_regex, phone):
                #     messages.info(r, "Not a valid phone number", extra_tags="placeorder")
                #     return redirect(checkout)
                #
                # # Validating pincode
                # if not re.match(pincode_regex, pincode):
                #     messages.info(r, "Not a valid pincode", extra_tags="placeorder")
                #     return redirect(checkout)
                pro = profile.objects.filter(user=user).first()
                if pro:

                    pro.fname = r.POST.get('fname')
                    pro.lname = r.POST.get('lname')
                    pro.email = r.POST.get('email')
                    pro.phone = r.POST.get('phone')
                    pro.address = r.POST.get('address')
                    pro.city = r.POST.get('city')
                    pro.state = r.POST.get('state')
                    pro.country = r.POST.get('country')
                    pro.pincode = r.POST.get('pincode')
                    pro.save()
                else:
                    cr = profile.objects.create(user=user, product_details=item, fname=fname, lname=lname, email=email,
                                                phone=phone,
                                                address=address, city=city, state=state, country=country,
                                                pincode=pincode)
                    cr.save()
                return redirect(placeorder)
            else:
                for i in c:
                    item = products.objects.get(pk=i.product_details.pk)
                    neworder = order()
                    neworder.user = user
                    neworder.product_details = item
                    # Assign order details from form data
                    neworder.fname = r.POST.get('fname')
                    neworder.lname = r.POST.get('lname')
                    neworder.email = r.POST.get('email')
                    neworder.phone = r.POST.get('phone')
                    neworder.address = r.POST.get('address')
                    neworder.city = r.POST.get('city')
                    neworder.state = r.POST.get('state')
                    neworder.country = r.POST.get('country')
                    neworder.pincode = r.POST.get('pincode')
                    neworder.total_price = item.price * i.quantity  # Calculate total price for this item
                    neworder.quantity = i.quantity  # Assign item quantity
                    neworder.payment_mode = r.POST.get('payment_mode')
                    neworder.payment_id = r.POST.get('payment_id')
                    # Generating a unique tracking number
                    trackno = 'ashion' + str(random.randint(1111111, 9999999))
                    while order.objects.filter(tracking_no=trackno).exists():
                        trackno = 'ashion' + str(random.randint(1111111, 9999999))
                    neworder.tracking_no = trackno
                    neworder.save()

                    # Creating order items for this item
                    orderitem.objects.create(
                        orderdet=neworder,
                        product=item,
                        price=item.price,
                        quantity=i.quantity
                    )

                # Clearing the cart after placing the order
                cart.objects.filter(user_details=user.id).delete()

                # Redirecting based on payment mode
                payMode = r.POST.get('payment_mode')
                if payMode == "Razorpay":
                    return JsonResponse({'status': 'Your order has been placed successfully'})
                else:
                    return redirect(thanku)

        return redirect(checkout)
def razorpaycheck(r):#main payment(means not for singlebuynow)
    if 'id' in r.session:
        user = userdetails.objects.get(username=r.session['id'])
        c = cart.objects.filter(user_details=user.id).all()
        t=0
        for i in c:
            t=t+(i.product_details.price * i.quantity)

    return JsonResponse({
        'total_price':t
    })


def checkout(r):
    if 'id' in r.session:
        user = userdetails.objects.get(username=r.session['id'])
        c = cart.objects.filter(user_details=user.id).all()
        wish_items = wishlist.objects.filter(user_details=user).count()
        if c:
            cnt = c.count()

            total_sum = 0  # Initialize total_sum variable
            for i in c:
                i.total_price = i.product_details.price * i.quantity
                total_sum += i.total_price

            usr = userdetails.objects.filter(id=user.id)
            det = profile.objects.filter(user=user).first()

            return render(r,'checkout.html',{'c':c,'det':det,'wish_items': wish_items,"usr":usr,'cnt':cnt,'total_sum': total_sum})
    return redirect(cart_details)
def cart_details(r):
 if 'id' in r.session:
     user=userdetails.objects.get(username=r.session['id'])
     data=cart.objects.filter(user_details=user)
     user1 = userdetails.objects.get(username=r.session['id'])
     count_items = cart.objects.filter(user_details=user1).count()
     print(count_items)
     user2 = userdetails.objects.get(username=r.session['id'])
     wish_items = wishlist.objects.filter(user_details=user2).count()
     print(wish_items)
     total_sum = 0  # Initialize total_sum variable
     for i in data:
         i.total_price = i.product_details.price * i.quantity
         total_sum += i.total_price

     return render(r, 'cart_details.html',{'data':data,'count_items': count_items,'wish_items': wish_items,'total_sum': total_sum})
 return redirect(login)


def increment_quantity(request, cart_id):
    cart_item = cart.objects.get(pk=cart_id)
    if cart_item.product_details.stock > 0:
        cart_item.quantity += 1
        cart_item.product_details.stock -= 1  # Decrease stock
        cart_item.save()
        cart_item.product_details.save()
        cart_item.total_price = cart_item.quantity * cart_item.product_details.price
        cart_item.save()

    else:
        messages.error(request, "Out of Stock  Cannot increase quantity.")
        # return HttpResponse("Out of Stock. Cannot increase quantity.")

    return redirect(cart_details)


def decrement_quantity(request, cart_id):
    cart_item = cart.objects.get(pk=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.product_details.stock += 1  # Increase stock
        cart_item.product_details.save()
        cart_item.save()

    else:
        messages.error(request, "Quantity cannot be less than 1")


    return redirect(cart_details)
def addcart(r,d):
    if 'id' in r.session:
        user=userdetails.objects.get(username=r.session['id'])
        prod=products.objects.get(pk=d)
        cart.objects.create(user_details=user,product_details=prod,total_price=prod.price).save()
        return redirect(cart_details)
    return redirect(login)
def remove(r, d):
        cart_item = cart.objects.get(pk=d)
        cart_item.delete()
        return redirect(cart_details)


#singlebuy starts
def checkoutbuynow(r):#single buy now checkout
    if 'id' in r.session:
        user = userdetails.objects.get(username=r.session['id'])
        c = buynow.objects.filter(user_details=user.id).all()
        wish_items = wishlist.objects.filter(user_details=user).count()
        if c:
            cnt = c.count()

            total_sum = 0  # Initialize total_sum variable
            for i in c:
                i.total_price = i.product_details.price * i.quantity
                total_sum += i.total_price

            usr = userdetails.objects.filter(id=user.id)
            det = profile.objects.filter(user=user).first()

            return render(r,'checkout2.html',{'c':c,'det':det,'wish_items': wish_items,"usr":usr,'cnt':cnt,'total_sum': total_sum})
    return redirect(buycart)
def placeorderbuynow(r):
    if 'id' in r.session:
        user = userdetails.objects.get(username=r.session['id'])
        c = buynow.objects.filter(user_details=user.id).all()

        t = 0
        for i in c:
            item = products.objects.get(pk=i.product_details.pk)
            t = t + (i.product_details.price * i.quantity)

        if r.method == 'POST':
            if r.POST.get('save') == 'save':
                # Validation and saving profile details
                # Code for validating and saving profile details...
                # This part remains unchanged
                fname = r.POST.get('fname')
                lname = r.POST.get('lname')
                email = r.POST.get('email')
                phone = r.POST.get('phone')
                address = r.POST.get('address')
                city = r.POST.get('city')
                state = r.POST.get('state')
                country = r.POST.get('country')
                pincode = r.POST.get('pincode')
                # phone_regex = r'^[6-9][0-9]{9}$'
                # pincode_regex = r'^[1-9][0-9]{5}$'
                #
                #
                # if not re.match(phone_regex, phone):
                #     messages.info(r, "Not a valid phone number", extra_tags="placeorder")
                #     return redirect(checkoutbuynow)
                #
                # # Validating pincode
                # if not re.match(pincode_regex, pincode):
                #     messages.info(r, "Not a valid pincode", extra_tags="placeorder")
                #     return redirect(checkoutoutbuynow)
                pro = profile.objects.filter(user=user).first()
                if pro:

                    pro.fname = r.POST.get('fname')
                    pro.lname = r.POST.get('lname')
                    pro.email = r.POST.get('email')
                    pro.phone = r.POST.get('phone')
                    pro.address = r.POST.get('address')
                    pro.city = r.POST.get('city')
                    pro.state = r.POST.get('state')
                    pro.country = r.POST.get('country')
                    pro.pincode = r.POST.get('pincode')
                    pro.save()
                else:
                    cr = profile.objects.create(user=user, product_details=item, fname=fname, lname=lname, email=email,
                                                phone=phone,
                                                address=address, city=city, state=state, country=country,
                                                pincode=pincode)
                    cr.save()
                return redirect(placeorder)
            else:
                for i in c:
                    item = products.objects.get(pk=i.product_details.pk)
                    neworder = order()
                    neworder.user = user
                    neworder.product_details = item
                    # Assign order details from form data
                    neworder.fname = r.POST.get('fname')
                    neworder.lname = r.POST.get('lname')
                    neworder.email = r.POST.get('email')
                    neworder.phone = r.POST.get('phone')
                    neworder.address = r.POST.get('address')
                    neworder.city = r.POST.get('city')
                    neworder.state = r.POST.get('state')
                    neworder.country = r.POST.get('country')
                    neworder.pincode = r.POST.get('pincode')
                    neworder.total_price = item.price * i.quantity  # Calculate total price for this item
                    neworder.quantity = i.quantity  # Assign item quantity
                    neworder.payment_mode = r.POST.get('payment_mode')
                    neworder.payment_id = r.POST.get('payment_id')
                    # Generating a unique tracking number
                    trackno = 'ashion' + str(random.randint(1111111, 9999999))
                    while order.objects.filter(tracking_no=trackno).exists():
                        trackno = 'ashion' + str(random.randint(1111111, 9999999))
                    neworder.tracking_no = trackno
                    neworder.save()

                    # Creating order items for this item
                    orderitem.objects.create(
                        orderdet=neworder,
                        product=item,
                        price=item.price,
                        quantity=i.quantity
                    )

                # Clearing the cart after placing the order
                buynow.objects.filter(user_details=user.id).delete()

                # Redirecting based on payment mode
                payMode = r.POST.get('payment_mode')
                if payMode == "Razorpay":
                    return JsonResponse({'status': 'Your order has been placed successfully'})
                else:
                    return redirect(thanku)

        return redirect(checkoutbuynow)
def addimage(r,d):
    if 'id' in r.session:
        user=userdetails.objects.get(username=r.session['id'])
        count_item = cart.objects.filter(user_details=user).values_list('product_details_id', flat=True)
        prod=products.objects.get(pk=d)
        count_items = cart.objects.filter(user_details=user).count()
        wish_items = wishlist.objects.filter(user_details=user).count()
        wish_item = wishlist.objects.filter(user_details=user).values_list('product_details_id', flat=True)
        # cart.objects.create(user_details=user, product_details=prod, total_price=prod.price).save()
        return render(r, 'view_product.html',
                      {'count_items': count_items,'count_item': count_item,'prod': prod,'wish_item': wish_item,'wish_items': wish_items})

    return redirect(login)

def addcarti(r,d):
    if 'id' in r.session:
        user=userdetails.objects.get(username=r.session['id'])
        prods=products.objects.get(pk=d)
        cart.objects.create(user_details=user,product_details=prods,total_price=prods.price).save()
        return redirect(cart_details)
    return redirect(login)
def buynowsi(r,prod_id):
    if 'id' in r.session:
        user = userdetails.objects.get(username=r.session['id'])
        product = products.objects.get(pk=prod_id)
        buynow.objects.create(user_details=user, product_details=product, total_price=product.price).save()
        return redirect(buycart)
    return redirect(login)

def removeb(r, d):
        cart_item = buynow.objects.get(pk=d)
        cart_item.delete()
        return redirect(buycart)

def buycart(r):
 if 'id' in r.session:
     user=userdetails.objects.get(username=r.session['id'])
     data=buynow.objects.filter(user_details=user)
     user1 = userdetails.objects.get(username=r.session['id'])
     count_items = cart.objects.filter(user_details=user1).count()
     print(count_items)
     user2 = userdetails.objects.get(username=r.session['id'])
     wish_items = wishlist.objects.filter(user_details=user2).count()
     print(wish_items)
     total_sum = 0  # Initialize total_sum variable
     for i in data:
         i.total_price = i.product_details.price * i.quantity
         total_sum += i.total_price

     return render(r, 'buynows.html',{'data':data,'count_items': count_items,'wish_items': wish_items,'total_sum': total_sum})
 return redirect(login)

def increment_quantity1(request, cart_id):
    cart_item = buynow.objects.get(pk=cart_id)
    if cart_item.product_details.stock > 0:
        cart_item.quantity += 1
        cart_item.product_details.stock -= 1  # Decrease stock
        cart_item.save()
        cart_item.product_details.save()
        cart_item.total_price = cart_item.quantity * cart_item.product_details.price
        cart_item.save()

    else:
        messages.error(request, "Out of Stock  Cannot increase quantity.")
        # return HttpResponse("Out of Stock. Cannot increase quantity.")

    return redirect(buycart)


def decrement_quantity1(request, cart_id):
    cart_item = buynow.objects.get(pk=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.product_details.stock += 1  # Increase stock
        cart_item.product_details.save()
        cart_item.save()

    else:
        messages.error(request, "Quantity cannot be less than 1")


    return redirect(buycart)

def razorpaycheck1(r):#singlebuy
    if 'id' in r.session:

        user = userdetails.objects.get(username=r.session['id'])
        c = buynow.objects.filter(user_details=user.id).all()

        t=0
        for i in c:
            t=i.product_details.price * i.quantity

    return JsonResponse({
        'total_price':t
    })

def addcart2(r,d):
    if 'id' in r.session:
        user=userdetails.objects.get(username=r.session['id'])

        prod=wishlist.objects.get(pk=d)
        product_details =  prod.product_details

        cart.objects.create(user_details=user,product_details=product_details,total_price=product_details.price).save()
        return redirect(cart_details)
    return redirect(login)
#ends one section
def view_product(request):
    image_url = request.GET.get('image_url')
    return render(request, 'view_product.html', {'image_url': image_url})


def wish(r):
   if 'id' in r.session:
      user=userdetails.objects.get(username=r.session['id'])

      data1=cart.objects.filter(user_details=user)
      user_wishlist1 = [item.product_details for item in data1]
      data=wishlist.objects.filter(user_details=user)
      user_wishlist = [item.product_details for item in data]
      count_items = cart.objects.filter(user_details=user).count()
      print(count_items)
      user2 = userdetails.objects.get(username=r.session['id'])
      wish_items = wishlist.objects.filter(user_details=user2).count()
      print(wish_items)
      return render(r, 'wish.html',{'data':data,'user_wishlist':user_wishlist,'user_wishlist1':user_wishlist1,'count_items':count_items,'wish_items':wish_items})
   return redirect(login)
def wishcart(r,d):
    if 'id' in r.session:
        user=userdetails.objects.get(username=r.session['id'])
        prod=products.objects.get(pk=d)
        wishlist.objects.create(user_details=user,product_details=prod).save()
        return redirect(wish)
    return redirect(login)
def removewish(r, d):
        cart_item = wishlist.objects.get(pk=d)
        cart_item.delete()
        return redirect(wish)
def wishcart2(r,d):#singlebuy
    if 'id' in r.session:
        user=userdetails.objects.get(username=r.session['id'])
        prod=products.objects.get(pk=d)
        wishlist.objects.create(user_details=user,product_details=prod).save()
        return redirect(wish)
    return redirect(login)


#adminside starts
def adminside(r):
 if 'id1' in r.session:
      if r.method == 'POST':
           category = r.POST['category']
           sizecategory = r.POST['sizecategory']
           product_name = r.POST['product_name']
           price = r.POST['price']
           size = r.POST['stock']
           description = r.POST['description']
           image = r.FILES['image']
           data = products.objects.create(category=category, description=description, product_name=product_name,
                                      price=price, stock=size, size=sizecategory ,image=image)
           data.save()
           messages.success(r, 'Data saved')
      out_of_stock_products = products.objects.filter(stock__lt=5)


      if out_of_stock_products.exists():
          admin_email = 'doniyaabraham@gmail.com'  # Change this to the admin's email address
          subject = 'Notification: Low Stock Products'
          message = 'The following products are low stock:\n\n'
          for product in out_of_stock_products:
              message += f'- {product.product_name}\n'
          send_mail(subject, message, 'noreply@example.com', [admin_email])

          for product in out_of_stock_products:
              message += f'- {product.product_name}: Current stock - {product.stock}\n'
          message += f'\nTimestamp: {datetime.datetime.now()}'
          send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [admin_email])
      data = products.objects.all()
      feedbk= feedback.objects.all()
      u = userdetails.objects.all()
      f = feedback.objects.all()

      rd = order.objects.all()
      o = orderitem.objects.all()
      return render(r, 'adminside.html', {'data':data,'feedbk':feedbk,'o':o,'rd':rd,'u':u,'f':f})
 return redirect(login)
def update(r,d):
  data = products.objects.get(pk=d)
  if r.method =='POST':
        print("**************")

        data.category = r.POST['category']
        data.product_name = r.POST['product_name']
        data.price = r.POST['price']
        data.stock = r.POST['stock']
        data.size= r.POST['sizecategory']
        data.description = r.POST['description']
        image = r.FILES['image']
        image1 = r.FILES['image1']
        image2 = r.FILES['image2']
        image3 = r.FILES['image3']
        if 'image' in r.FILES:
            data.image = r.FILES['image']
        if 'image1' in r.FILES:
            data.image1 = r.FILES['image1']
        if 'image2' in r.FILES:
            data.image2 = r.FILES['image2']
        if 'image3' in r.FILES:
            data.image3 = r.FILES['image3']


        data.save()
        messages.success(r, 'updated')
        return redirect(adminside)

  return render(r, 'update.html', {'data': data, })

def update1(r,d):#status update of order
    if r.method =='POST':
        print("**************")
        category = r.POST['category']

        order.objects.filter(pk=d).update( statuss= category)
        messages.success(r, 'updated')
        return redirect(adminside)
    if 'id1' in r.session:
        data =  order.objects.get( pk=d)
        return render(r, 'update1.html', {'data': data})

    else:
        return HttpResponse("User id not found in session.")




def delete(r, d):
        data = products.objects.get(pk=d)
        data.delete()
        messages.error(r, 'delete suceesfully')
        return redirect(adminside)


def delete1(r, d):
    data = order.objects.get(pk=d)
    data.delete()
    messages.error(r, 'delete suceesfully')
    return redirect(adminside)
def booking_dtls(r):
    user=userdetails.objects.get(username=r.session['id'])
    book=bookings.objects.filter(user_details=user)
    return render(r,'booking_dtls.html',{'book':book})




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = userdetails.objects.get(email=email)
        except:
            messages.info(request,"Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}','settings.EMAIL_HOST_USER', [email],fail_silently=False)
            return render(request, 'emailsent.html')
        except:
            messages.info(request,"Network connection failed")
            return redirect(forgot_password)

    return render(request, 'password_reset_sent.html')
def reset_password(request, token):
    # Verify token and reset the password
    password_reset = PasswordReset.objects.get(token=token)
    usr = userdetails.objects.get(id=password_reset.user_id)
    return render(request, 'reset_password.html',{'token':token})

def reset_password2(request, token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    usr = userdetails.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('repeatpassword')
        if repeat_password == new_password:
            password_reset.user.password = new_password
            password_reset.user.save()
            password_reset.delete()
            send_confirmation_email(usr.email)
            return redirect(login)
    return render(request, 'reset_password.html')

def send_confirmation_email(email):
    subject = 'Password Changed Successfully'
    message = 'Your password has been changed successfully. If you did not request this change, please contact us immediately.'
    send_mail(subject, message, 'doniyaabraham@gmail.com', [email])
def reply(r, em):
    l = feedback.objects.filter(id=em).first()
    return render(r, "replymail.html", {'l': l})


def replymail(r, em):
    if r.method == 'POST':
        l = feedback.objects.filter(id=em).first()
        n = r.POST.get('message')
        try:
            send_mail('Reply from ashion wedding  ', f'{n}', settings.EMAIL_HOST_USER, [l.email], fail_silently=False)
            return redirect(adminside)
        except :
            ms = "NETWORK CONNECTION FAILED"
            messages.info(r, "Network connection failed")
            return render(r, 'replymail.html', {"ms": ms})

    return render(r, 'replymail.html')

