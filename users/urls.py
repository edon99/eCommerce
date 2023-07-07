from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ProductListView,OrderDeleteView
urlpatterns = [
    path('sellerHome/', views.sellerHome, name='seller-home'),
    path('sellerProducts/', ProductListView.as_view(), name='seller-products'),
    path('sellerDashboard/', views.analytics, name='seller-dashboard'),
    path('sellerOrders/', views.sellerOrders, name='seller-orders'),
    path('sellerOrders/<int:pk>/update/',views.OrderUpdate , name='order-update'),
    path('sellerOrders/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    
]