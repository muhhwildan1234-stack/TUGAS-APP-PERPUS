from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from .models import Buku, Peminjaman, Anggota

# ==========================================
# 1. HALAMAN DASHBOARD MAIN
# ==========================================
def dashboard(request):
    total_buku = Buku.objects.aggregate(total=Sum('stok'))['total'] or 0
    total_judul = Buku.objects.count()
    sedang_dipinjam = Peminjaman.objects.filter(status='Dipinjam').count()
    sudah_dikembalikan = Peminjaman.objects.filter(status='Dikembalikan').count()
    
    buku_list = Buku.objects.all()[:3]
    
    context = {
        'total_buku': total_buku,
        'total_judul': total_judul,
        'sedang_dipinjam': sedang_dipinjam,
        'sudah_dikembalikan': sudah_dikembalikan,
        'buku_list': buku_list,
    }
    return render(request, 'perpus/dashboard.html', context)


# ==========================================
# 2. MANAJEMEN USER (ANGGOTA)
# ==========================================
def daftar_user(request):
    users = Anggota.objects.all()
    return render(request, 'perpus/daftar_user.html', {'users': users})

def tambah_user(request):
    if request.method == 'POST':
        nama_input = request.POST.get('nama')
        kelas_input = request.POST.get('kelas')
        nis_input = request.POST.get('nis')
        status_raw = request.POST.get('status') # 'aktif' / 'nonaktif' dari HTML
        
        # Mapping status agar sesuai dengan Pilihan Kapital di Model
        status_input = 'Aktif' if status_raw == 'aktif' else 'Tidak Aktif'
        
        Anggota.objects.create(
            nama=nama_input,
            kelas=kelas_input,
            nis=nis_input,
            status=status_input
        )
        return redirect('daftar_user')
        
    return render(request, 'perpus/tambah_user.html')


# ==========================================
# 3. MANAJEMEN BUKU
# ==========================================
def daftar_buku(request):
    buku_all = Buku.objects.all()
    return render(request, 'perpus/daftar_buku.html', {'buku_all': buku_all})

def tambah_buku(request):
    if request.method == 'POST':
        Buku.objects.create(
            judul=request.POST.get('judul'),
            pengarang=request.POST.get('penulis'),
            kategori=request.POST.get('kategori'),
            penerbit=request.POST.get('penerbit'),
            tahun_terbit=request.POST.get('tahun_terbit'),
            stok=request.POST.get('stok'),
        )
        return redirect('daftar_buku')
    return render(request, 'perpus/edit_buku.html', {'aksi': 'Tambah'})

def detail_buku(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    return render(request, 'perpus/detail_buku.html', {'buku': buku})

def edit_buku(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.judul = request.POST.get('judul')
        buku.pengarang = request.POST.get('penulis')
        buku.kategori = request.POST.get('kategori')
        buku.penerbit = request.POST.get('penerbit')
        buku.tahun_terbit = request.POST.get('tahun_terbit')
        buku.stok = request.POST.get('stok')
        buku.save()
        return redirect('daftar_buku')
    return render(request, 'perpus/edit_buku.html', {'buku': buku, 'aksi': 'Edit'})

def hapus_buku(request, pk):
    buku = get_object_or_404(Buku, pk=pk)
    if request.method == 'POST':
        buku.delete()
        return redirect('daftar_buku')
    return render(request, 'perpus/hapus_buku.html', {'buku': buku})


# ==========================================
# 4. MANAJEMEN PEMINJAMAN
# ==========================================
def peminjaman(request):
    # Mengambil data peminjaman diurutkan dari yang terbaru
    peminjaman_all = Peminjaman.objects.all().order_by('-id')
    return render(request, 'perpus/peminjaman.html', {'peminjaman_all': peminjaman_all})
def pinjam_buku(request):
    if request.method == 'POST':
        anggota_id = request.POST.get('anggota')
        buku_id = request.POST.get('buku')
        tanggal_pinjam = request.POST.get('tanggal_pinjam')
        # Ambil data dari form HTML
        jatuh_tempo_input = request.POST.get('jatuh_tempo') 
        keperluan = request.POST.get('keperluan')
        keterangan_keperluan = request.POST.get('keterangan_keperluan')
        petugas = request.POST.get('petugas')

        anggota = get_object_or_404(Anggota, id=anggota_id)
        buku = get_object_or_404(Buku, id=buku_id)

        if buku.stok >= 1:
            Peminjaman.objects.create(
                anggota=anggota,
                buku=buku,
                tanggal_pinjam=tanggal_pinjam,
                # PASTIKAN DI SINI MENGGUNAKAN jatuh_tempo, BUKAN tanggal_kembali
                jatuh_tempo=jatuh_tempo_input, 
                keperluan=keperluan,
                keterangan_keperluan=keterangan_keperluan,
                petugas=petugas,
                status='Dipinjam'
            )
            buku.stok -= 1
            buku.save()
            
        return redirect('peminjaman')

    users_all = Anggota.objects.filter(status='Aktif')
    buku_all = Buku.objects.all()
    return render(request, 'perpus/pinjam_buku.html', {'users_all': users_all, 'buku_all': buku_all})

def kembalikan_buku(request, pk):
    transaksi = get_object_or_404(Peminjaman, pk=pk)
    if transaksi.status == 'Dipinjam' or transaksi.status == 'Terlambat':
        # Kembalikan stok buku
        buku = transaksi.buku
        buku.stok += 1
        buku.save()
        
        # Ubah status transaksi
        transaksi.status = 'Dikembalikan'
        transaksi.save()
        
    return redirect('peminjaman')