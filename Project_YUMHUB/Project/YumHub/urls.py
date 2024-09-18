from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login/",views.login,name='login'),
    path("signup/",views.signup,name='signup'),
    path("menu/",views.menu,name='menu'),
    path("checkout/",views.checkout,name='checkout'),
    path("payment/",views.payment,name='payment'),
    path("bill/",views.bill,name='bill'),
    path("admin_dashboard/",views.admin_dashboard,name='admin_dashboard'),
    # path("progress/",views.progress,name='progress'),
    path("logout/",views.logout_view,name="logout")
]
