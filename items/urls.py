"""items URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r"^$", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r"^$", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r"^blog/", include("blog.urls"))
"""
from django.conf.urls import url, include

from rest_framework import routers

from . import views


ROUTER = routers.DefaultRouter()
ROUTER.register(r"brands", views.BrandViewSet)
ROUTER.register(r"stores", views.StoreViewSet)
ROUTER.register(r"orders", views.OrderViewSet)
ROUTER.register(r"items", views.ItemViewSet)
ROUTER.register(r"locations", views.LocationViewSet)
ROUTER.register(r"purchases", views.PurchaseViewSet)


urlpatterns = [  # pylint: disable=invalid-name
    url(r"^", include(ROUTER.urls)),
]
