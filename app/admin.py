from django.contrib import admin
from django.urls import reverse
from . models import Contact, Menu, Customer, Cart, OrderPlaced, Payment
from django.utils.html import format_html
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(Menu)
class MenuModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_image', 'product_name', 'product_price','category']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','mobile','tablenumber']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','products','quantity']
    def products(self,obj):
        link = reverse('admin:app_menu_change',args=[obj.menu.pk])
        return format_html('<a href="{}">{}</a>',link, obj.menu.product_name)


@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid']


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','products','quantity','ordered_date','status','payments']
    def customers(self,obj):
        link=reverse('admin:app_customer_change',args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>',link,obj.customer.name)
    
    def payments(self,obj):
        link=reverse('admin:app_payment_change',args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>',link,obj.payment.razorpay_payment_id)
    


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','message']


admin.site.unregister(Group)