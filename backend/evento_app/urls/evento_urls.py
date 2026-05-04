from django.urls import path
from ..views.evento_views import evento_actual

urlpatterns = [
 
    path('evento-actual/', evento_actual, name='evento_actual'),
  
]