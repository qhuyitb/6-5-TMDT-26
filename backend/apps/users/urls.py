from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    CartView,
    CartItemAddView,
    CartItemUpdateView,
    CartItemDeleteView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('cart/', CartView.as_view(), name='api_cart'),
    path('cart/items/', CartItemAddView.as_view(), name='api_cart_item_add'),
    path('cart/items/<int:item_id>/', CartItemUpdateView.as_view(), name='api_cart_item_update'),
    path('cart/items/<int:item_id>/delete/', CartItemDeleteView.as_view(), name='api_cart_item_delete'),
]
