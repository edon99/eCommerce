from django.conf import settings
from django.conf.urls.static import static
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView ,home,SuccessView,OrderCreateView,CreateCheckoutSessionView
from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home, name='site-home'),
    path('', home.as_view(), name='site-home'),
    path('about/', views.about, name='site-about'),
    path('products/', ProductListView.as_view(), name='site-products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('products/new/', ProductCreateView.as_view(), name='product-create'),
    path('products/<int:pk>/order/', OrderCreateView.as_view(), name='order-create'),
    path('products/<int:pk>/checkout', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('products/<int:pk>/<int:order_id>/payment/', views.Payment, name='payment'),
    path('products/order/success/<int:pk>/', SuccessView.as_view(), name='success'),
    path('orders/', views.orders, name='user-orders'),
]