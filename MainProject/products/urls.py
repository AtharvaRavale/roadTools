# from django.urls import path
# from . import views

# urlpatterns = [
#     path('products/', views.products, name='products'),
# ]


from django.urls import path
from .views import products, edit_product, delete_product

urlpatterns = [
    path('products/', products, name='products'),
    path('edit-product/<int:product_id>/', edit_product, name='edit_product'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
]
