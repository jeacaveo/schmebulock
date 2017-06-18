"""schmebulock URL Configuration

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
from django.contrib import admin

from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view

from items import views as item_views


ROUTER = routers.DefaultRouter()
ROUTER.register(r"brands", item_views.BrandViewSet)
ROUTER.register(r"stores", item_views.StoreViewSet)
ROUTER.register(r"orders", item_views.OrderViewSet)
ROUTER.register(r"items", item_views.ItemViewSet)
ROUTER.register(r"locations", item_views.LocationViewSet)
ROUTER.register(r"purchases", item_views.PurchaseViewSet)


urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^api/auth/",
        include("rest_framework.urls", namespace="rest_framework")),
    url(r"^api/auth/token/", obtain_jwt_token),
    url(r"^api/docs/", get_swagger_view(title="Schmebulock API")),
    url(r"^api/", include(ROUTER.urls)),
]
