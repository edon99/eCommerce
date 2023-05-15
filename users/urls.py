from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ProductListView
urlpatterns = [
    path('sellerHome/', views.sellerHome, name='seller-home'),
    path('sellerProducts/', ProductListView.as_view(), name='seller-products'),
     path('sellerAnalytics/', views.analytics, name='seller-analytics'),
    
]