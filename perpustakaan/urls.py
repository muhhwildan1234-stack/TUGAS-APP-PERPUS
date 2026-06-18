from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Mengarahkan seluruh URL utama langsung ke file urls.py milik aplikasi perpus
    path('', include('perpus.urls')), 
]