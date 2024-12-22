from django.db.models import Count
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
import razorpay
from . models import Cart, Contact, Customer, Menu, OrderPlaced, Payment
from . forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
def home(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        data=Contact(name=name,email=email,message=message)
        data.save()
    return render(request, "app/home.html")

@login_required
def user(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')
        data=Contact(name=name,email=email,message=message)
        data.save()
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    
    return render(request, "app/user.html",locals())


@method_decorator(login_required,name='dispatch')
class MenuView(View):
    def get(self,request,val):
        menu = Menu.objects.filter(category=val)
        product_name = Menu.objects.filter(category=val).values('product_name')
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/menu.html",locals())
    

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request, "app/signup.html",locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! SignIn Successfully,LogIn Now")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, "app/signup.html",locals())        


@method_decorator(login_required,name='dispatch')   
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            tablenumber = form.cleaned_data['tablenumber']

            reg = Customer(user=user,name=name,mobile=mobile,tablenumber=tablenumber)
            reg.save()
            messages.success(request,"Profile save Successfully!, Go to Home.")
        else:
            messages.warning(request,"Invalid Input Data")    
        return render(request, 'app/profile.html', locals())


@login_required    
def details(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/userdetails.html',locals())


@method_decorator(login_required,name='dispatch')
class updateDetails(View):
    def get(self,request,pk):
        add =Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updatedetails.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.mobile = form.cleaned_data['mobile']
            add.tablenumber = form.cleaned_data['tablenumber']
            add.save()
            messages.success(request,"Congratulations! Profile Update Successfully.")
        else:
            messages.warning(request,"Invalid Input Data")    
        return redirect('userdetails')
    

@login_required
def logout(request):
    request.session.clear()
    return redirect('login')


@login_required
def add_to_cart(request):
    user = request.user
    products_id = request.GET.get('prod_id')
    products = Menu.objects.get(id=products_id)
    Cart(user=user,products=products).save()
    return redirect("/cart")


@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.products.product_price
        amount = amount + value
    totalamount = amount + 10     
    return render(request, 'app/addtocart.html',locals())


@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.products.product_price
            famount = famount  + value
        totalamount = famount + 10    
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = { "amount": razoramount,"currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
       # {'amount': 8000, 'amount_due': 8000, 'amount_paid': 0, 'attempts': 0, 'created_at': 1734712091, 'currency': 'INR', 'entity': 'order', 'id': 'order_PZUqO9moLrxFmW', 'notes': [], 'offer_id': None, 'receipt': 'order_rcptid_12', 'status': 'created'}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'app/checkout.html',locals())


@login_required
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')
    cust_id=request.GET.get('cust_id')
    user=request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,products=c.products,quantity=c.quantity,payment=payment).save()
        c.delete()
    return redirect("orders")    


@login_required
def orders(request):
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', locals())


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.products.product_price
            amount = amount + value
        totalamount = amount + 10 
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.products.product_price
            amount = amount + value
        totalamount = amount + 10 
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)
    

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(products=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.products.product_price
            amount = amount + value
        totalamount = amount + 10 
        data = {
            'amount':amount,
            'totalamount':totalamount,
        }
        return JsonResponse(data)