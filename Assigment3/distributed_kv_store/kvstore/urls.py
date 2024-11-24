from django.urls import path
from .views import *

urlpatterns = [
    path('kv/<str:key>/', get_data, name='get_data'),
    path('kv/', set_data, name='set_data'),
]