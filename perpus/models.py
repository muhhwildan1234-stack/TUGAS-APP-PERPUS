from django.db import models

# 1. Tabel Buku
class Buku(models.Model):
    judul = models.CharField(max_length=255)
    pengarang = models.CharField(max_length=255)
    penerbit = models.CharField(max_length=255)
    tahun_terbit = models.IntegerField()
    kategori = models.CharField(max_length=100)
    stok = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.judul} - {self.pengarang}"


# 2. Tabel Anggota/User
class Anggota(models.Model):
    STATUS_CHOICES = [
        ('Aktif', 'Aktif'),
        ('Tidak Aktif', 'Tidak Aktif'),
    ]
    
    nama = models.CharField(max_length=255)
    kelas = models.CharField(max_length=50)  
    nis = models.CharField(max_length=20, unique=True)  
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Aktif')

    def __str__(self):
        return self.nama


# 3. Tabel Peminjaman
class Peminjaman(models.Model):
    STATUS_PINJAM = [
        ('Dipinjam', 'Dipinjam'),
        ('Dikembalikan', 'Dikembalikan'),
        ('Terlambat', 'Terlambat'),
    ]

    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE, related_name='peminjaman')
    buku = models.ForeignKey(Buku, on_delete=models.CASCADE, related_name='peminjaman')
    
    tanggal_pinjam = models.DateField()
    jatuh_tempo = models.DateField()
    keperluan = models.CharField(max_length=255, default='Bacaan pribadi')
    keterangan_keperluan = models.TextField(blank=True, null=True)
    petugas = models.CharField(max_length=100, default='Budi Siregar')
    status = models.CharField(max_length=15, choices=STATUS_PINJAM, default='Dipinjam')
    denda = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.anggota.nama} meminjam {self.buku.judul}"