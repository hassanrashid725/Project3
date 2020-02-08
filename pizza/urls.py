from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login, name = "login"),
    path("signup", views.signup, name = "signup"),
    path("order", views.order, name = "order"),
    path("contact", views.contact, name = "contact"),
    path("about", views.about, name = "about"),
    url(r'^checkout/$', views.checkout, name = "checkout"),
    url(r'^getmenu/$', views.getMenu, name='getmenu'),   # getMenu view at /getmenu
    url(r'^getcategories/$', views.getCategories, name='getcatagories'), # getCategories view at /getcategories
    url(r'^getsubsextraprices/$', views.getSubsExtraPrices, name='getsubsextraprices'), # getSubsExtraPrices view at /getsubsextraprices
  ]
