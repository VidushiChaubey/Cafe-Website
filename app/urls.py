from django.urls import path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordResetForm, MyPasswordChangeForm, MySetPasswordForm


urlpatterns = [
    path("", views.home),
    path("user/", views.user),
    path("menu/<slug:val>", views.MenuView.as_view(),name="menu"),
    path("profile/", views.ProfileView.as_view(), name='profile'),
    path("details/", views.details, name='userdetails'),
    path('updatedetails/<int:pk>',views.updateDetails.as_view(), name='updatedetails'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),

    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),


#login authentication
    path("signup/", views.CustomerRegistrationView.as_view(),name='signup'),
    path("accounts/login/", auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm) , name='login'), 
    path("passwordchange/",auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/',views.logout, name='logout'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "CafeADR"
admin.site.site_title = "CafeADR"
admin.site.site_index_title = "Welcome to CafeADR"