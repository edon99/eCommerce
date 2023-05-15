from django.conf import settings
from django.conf.urls.static import static
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView ,home
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
    

]