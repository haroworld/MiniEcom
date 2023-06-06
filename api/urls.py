from django.urls import path
from . import views
from .views import RegisterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),

    path('', views.getRoutes),
    path('products/', views.getProducts),
    path('products/<str:pk>/', views.getProduct),
    path('cart/', views.getCart),
    path('update_item/', views.updateItem),
    path('process_order/', views.processOrder),
    
]