from django.contrib import admin
from .models import Buku, Anggota, Peminjaman

class BukuAdmin(admin.ModelAdmin):
    list_display = ('judul', 'pengarang', 'penerbit', 'tahun_terbit', 'stok')
    search_fields = ('judul', 'pengarang')

class AnggotaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kelas', 'nis', 'status')
    search_fields = ('nama', 'nis')

class PeminjamanAdmin(admin.ModelAdmin):
    # PERBAIKAN: 'tanggal_kembali' diubah menjadi 'jatuh_tempo'
    list_display = ('anggota', 'buku', 'tanggal_pinjam', 'jatuh_tempo', 'status', 'denda')
    list_filter = ('status', 'tanggal_pinjam')

# Daftarkan model ke Admin Django
admin.site.register(Buku, BukuAdmin)
admin.site.register(Anggota, AnggotaAdmin)
admin.site.register(Peminjaman, PeminjamanAdmin)