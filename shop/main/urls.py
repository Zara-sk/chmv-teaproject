from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [

    path(
        '',
        views.HomepageView.as_view(),
        name='homepage'
    ),

    path(
        'products/<str:slug>/',
        views.ProductDetailView.as_view(),
        name='product_detail'
    ),

    path(
        'category/<str:slug>/',
        views.CategoryDetailView.as_view(),
        name='category_detail'
    ),

    path(
        'cart/',
        views.CartView.as_view(),
        name='cart'
    ),

    path(
        'add-to-cart/<str:slug>/',
        views.AddToCartView.as_view(),
        name='add_to_cart'
    ),

    path(
        'cart/delete-from-cart/<str:slug>/',
        views.DeleteFromCartView.as_view(),
        name='delete_from_cart'
    ),

    path(
        'cart/change-qty-cart/<str:slug>/',
        views.ChangeQTYView.as_view(),
        name='change_qty_cart'
    ),

    path(
        'checkout/',
        views.CheckOutView.as_view(),
        name='checkout'
    ),

    path(
        'make-order/',
        views.MakeOrderView.as_view(),
        name='make_order'
    ),

    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),

    path(
        'registrarion/',
        views.RegistrationView.as_view(),
        name='registration'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='/login/'),
        name='logout'
    ),

    path(
        'orders/',
        views.OrdersView.as_view(),
        name='orders'
    )
]
