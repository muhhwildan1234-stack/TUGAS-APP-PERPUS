from django.urls import path
from . import views # Ini akan mengambil views.py yang ada di dalam folder perpus

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('user/', views.daftar_user, name='daftar_user'),
    path('user/tambah/', views.tambah_user, name='tambah_user'),
    path('buku/', views.daftar_buku, name='daftar_buku'),
    path('buku/tambah/', views.tambah_buku, name='tambah_buku'),
    path('buku/detail/<int:pk>/', views.detail_buku, name='detail_buku'),
    path('buku/edit/<int:pk>/', views.edit_buku, name='edit_buku'),
    path('buku/hapus/<int:pk>/', views.hapus_buku, name='hapus_buku'),
    path('peminjaman/', views.peminjaman, name='peminjaman'),
    path('peminjaman/baru/', views.pinjam_buku, name='pinjam_buku'),
    path('peminjaman/kembali/<int:pk>/', views.kembalikan_buku, name='kembalikan_buku'),
]