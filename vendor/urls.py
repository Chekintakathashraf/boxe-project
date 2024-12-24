
from django.urls import path
from .views import *
app_name = 'vendor'
urlpatterns = [
    path('', vendor_list, name='vendor_list'), 
    path('create/', create_vendor, name='create_vendor'),  
    path('<int:vendor_id>/update/', update_vendor, name='update_vendor'), 
    path('<int:vendor_id>/delete/', delete_vendor, name='delete_vendor'),  
]