from django.db import models

# Create your models here.
class userdetails(models.Model):
    firstname=models.CharField(max_length=10)
    lastname=models.CharField(max_length=10)
    email=models.EmailField()
    phno=models.IntegerField()
    username = models.CharField(max_length=18)
    password = models.CharField(max_length=10)
    address = models.CharField(max_length=10)

    def __str__(self):
        return self.firstname
class products(models.Model):
    category=models.CharField(max_length=10)
    description =models.CharField(max_length=600)
    product_name=models.CharField(max_length=15)
    price=models.IntegerField()
    stock=models.IntegerField()
    image=models.FileField()
    image1 = models.FileField()
    image2 = models.FileField()
    image3 = models.FileField()
    size=models.CharField(max_length=10)


class buynow(models.Model):
    product_details=models.ForeignKey(products,on_delete=models.CASCADE)
    user_details=models.ForeignKey(userdetails,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.IntegerField()

class cart(models.Model):
    product_details=models.ForeignKey(products,on_delete=models.CASCADE)
    user_details=models.ForeignKey(userdetails,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.IntegerField()

    # Add this line

    def subtotal(self):
        return self.product_details.price * self.quantity

ORDERSTATUS=(
        (1,'Pending'), (2,'Dispatch'),
        (3,'On the way'), (4,'Delivered'),(5,'Cancelled'),(6,'Return')
    )
class order(models.Model):
    user = models.ForeignKey(userdetails,on_delete=models.CASCADE)
    product_details = models.ForeignKey(products, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=150, null=True)
    orderstatus = (
        ('Pending', 'Pending'),
        ('Out for shipping', 'Out for shipping'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )#nil
    quantity = models.PositiveIntegerField(default=1)

    statuss = models.IntegerField(choices=ORDERSTATUS, default=1)
    status = models.CharField(max_length=150, choices=orderstatus, default='pending')#nil
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.tracking_no}'

class profile(models.Model):
    user = models.OneToOneField(userdetails,on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False)
    lname = models.CharField(max_length=150, null=False)
    email = models.CharField(max_length=150, null=False)
    phone = models.CharField(max_length=150, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}'

class wishlist(models.Model):
    product_details = models.ForeignKey(products, on_delete=models.CASCADE)
    user_details = models.ForeignKey(userdetails, on_delete=models.CASCADE)


class bookings(models.Model):#not using this model
    user_details = models.ForeignKey(userdetails, on_delete=models.CASCADE)
    item_details = models.ForeignKey(products, on_delete=models.CASCADE)
    address=models.CharField(max_length=150,null='amayoor')
    city = models.CharField(max_length=150, null='kochi')
    state = models.CharField(max_length=150, null='kerala')
    country = models.CharField(max_length=150, null='india')

    date = models.DateField()
    quantity = models.IntegerField()
    track=models.CharField(max_length=20,default='Not Paid')
    total_price = models.IntegerField()
    status=models.CharField(max_length=20,default='Shipped')

class orderitem(models.Model):#nil
    orderdet = models.ForeignKey(order,on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self) -> str:
        return f'{self.orderdet}'


class feedback(models.Model):
    name=models.CharField(max_length=10)
    email=models.EmailField()
    messg = models.CharField(max_length=50)
class PasswordReset(models.Model):
    user = models.ForeignKey(userdetails, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
