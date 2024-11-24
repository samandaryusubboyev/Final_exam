from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.CategoriesView.as_view(), name='categories'),
    path('products/<int:category_id>/', views.ProductsView.as_view(), name='products'),
    path('detail/<int:product_id>/', views.product_detail, name='detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('change_product_cart/<int:product_id>/<str:action>/', views.change_product_cart, name='change_product_cart'),





]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)