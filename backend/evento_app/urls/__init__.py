from django.urls import include, path
from . import auth_urls, evento_urls, participante_urls, oponente_urls

urlpatterns = [
    path('', include(auth_urls)),
    path('', include(evento_urls)),
    path('', include(participante_urls)),
    path('', include(oponente_urls)),
]