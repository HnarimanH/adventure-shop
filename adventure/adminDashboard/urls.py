from django.urls import path
from .views import CreateProductView, ProductView
urlpatterns = [
    path('createproduct/', CreateProductView.as_view(), name = 'createproduct' ),
    path('showproduct/', ProductView.as_view(), name = 'showproduct' )
]
