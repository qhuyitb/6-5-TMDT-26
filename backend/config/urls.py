"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TemplateView.as_view(template_name='pages/login/login.html'), name='login_page'),
    path('products/', TemplateView.as_view(template_name='pages/products/products.html'), name='products_page'),
    path('shop/', TemplateView.as_view(template_name='pages/shop/shop.html'), name='shop_page'),
    path('cart/', TemplateView.as_view(template_name='pages/cart/cart.html'), name='cart_page'),
    path('api/auth/', include('apps.users.urls')),
    path('api/', include('apps.products.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

