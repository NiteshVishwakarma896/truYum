from django.urls import path
from .  import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('menu/admin', views.menu_list_admin, name='menu'),
    path('menu/admin/edit/<int:id>', views.edit_menu_item, name='edit'),
    path('menu/admin/edit/status', views.menu_item_status, name='item-status'),
    #customer urls
    path('customer/menu',views.menu_list_customer, name="customer-menu"),
    path('customer/cart/add/<int:id>/<str:name>/<str:price>/<str:category>/<str:delivery>',views.cart_list_customer_add, name="customer-cart-add"),
    path('customer/cart',views.cart_list_customer, name="customer-cart"),
    path('customer/cart/delete/<int:id>',views.delete_cart_item, name="customer-cart-delete"),
    path('logout',views.logout, name="logout"),
]