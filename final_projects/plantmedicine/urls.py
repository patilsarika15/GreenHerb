from unicodedata import name
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('predict/', views.predict_plant, name='predict'),
    path('search_plant/', views.search_plant, name='search'),
    path('text/',views.text,name='text'),
    path('imagePlant/',views.imagePlant,name='imagePlant'),
    
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
