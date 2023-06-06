from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('product/<str:pk>/', views.viewProduct, name="product"),
    path('order', views.cart, name="order"),
    path('checkout', views.checkout, name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),

    path('login/', views.loginUser, name="login"),
    path('logout/', views.Logout, name="logout"),
    path('register/', views.registerUser, name="register")
]