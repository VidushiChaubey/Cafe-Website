from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORY_CHOICES=(
    ('HB','Hot-Beverages'),
    ('CB','Cold-Beverages'),
    ('RF','Refreshment'),
    ('SC','Special-Combos'),
    ('DE','Dessert'),
    ('BF','Burger-&-FrenchFries'),
)

NUMBER_CHOICES=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
    ('8','8'),
    ('9','9'),
    ('10','10'),
    ('11','11'),
)

class Menu(models.Model):
    product_image=models.ImageField(upload_to='product')
    product_name=models.CharField(max_length=100)
    product_price=models.FloatField()
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    def __str__(self):
        return self.product_name
    

class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.IntegerField(default=0)
    tablenumber = models.CharField(choices=NUMBER_CHOICES,max_length=100)
    def __str__(self):
        return self.name
    


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Menu,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.products.product_price
    

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Making','Making'),
    ('On The Way','On The Way'),
    ('Served','Served'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    products = models.ForeignKey(Menu,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE, default="")
    @property
    def total_cost(self):
        return self.quantity * self.products.product_price 
    

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=60)
    message = models.TextField()