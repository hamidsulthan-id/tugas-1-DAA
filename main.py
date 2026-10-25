import csv
import math
import time

from kelas import SearchInput, SearchResult, baca_csv, urutkan_judul

NAMA_FILE_CSV = "google_books_dataset.csv"


JUDUL_CONTOH = "Regulation of Liquor Traffic, District of Columbia"                # buku yang ADA di dataset
JUDUL_TIDAK_ADA = "Antek antek asing"   # buku yang TIDAK ada di dataset

UKURAN_INPUT = [100, 1000, 10000]
ULANG_WAKTU = 200          # waktu tiap pencarian diukur 200 kali lalu dirata-rata


# =====================================================================
# BAGIAN 3. LINEAR SEARCH  
# =====================================================================
def linear_search(data_in: SearchInput) -> SearchResult:
    data = data_in.dataset
    kunci = data_in.keyword.strip().lower()
    perbandingan = 0

    mulai = time.perf_counter()
    for i in range(len(data)):
        perbandingan += 1
        if data[i].judul_kunci == kunci:
            selesai = time.perf_counter()
            return SearchResult(True, data[i], i, perbandingan, selesai - mulai)
    selesai = time.perf_counter()
    return SearchResult(False, None, -1, perbandingan, selesai - mulai)


# =====================================================================
# BAGIAN 4. BINARY SEARCH 
# =====================================================================
def binary_search(data_in: SearchInput) -> SearchResult:
    data = data_in.dataset
    kunci = data_in.keyword.strip().lower()
    kiri, kanan = 0, len(data) - 1
    perbandingan = 0

    mulai = time.perf_counter()
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        perbandingan += 1
        nilai = data[tengah].judul_kunci
        if nilai == kunci:
            selesai = time.perf_counter()
            return SearchResult(True, data[tengah], tengah, perbandingan, selesai - mulai)
        elif nilai < kunci:
            kiri = tengah + 1          # buang separuh kiri
        else:
            kanan = tengah - 1         # buang separuh kanan
    selesai = time.perf_counter()
    return SearchResult(False, None, -1, perbandingan, selesai - mulai)


# =====================================================================
# BAGIAN 5. TAMPILKAN HASIL 
# =====================================================================
def cetak_hasil(res: SearchResult):
    if res.ditemukan:
        b = res.buku
        print(f"  DITEMUKAN di indeks {res.indeks}")
        print(f"  Judul    : {b.judul}")
        print(f"  Penulis  : {b.penulis}")
        print(f"  Kategori : {b.kategori}")
        print(f"  Rating   : {b.rating}")
        print(f"  Harga    : {b.harga}")
    else:
        print("  Buku TIDAK ditemukan di dataset.")
    print(f"  Jumlah perbandingan: {res.jumlah_perbandingan}")


def demo(buku, buku_urut):
    for kunci, label in [(JUDUL_CONTOH, "DITEMUKAN"), (JUDUL_TIDAK_ADA, "TIDAK DITEMUKAN")]:
        print(f"\n=== Kasus {label}: '{kunci}' ===")
        print("[Linear Search]")
        cetak_hasil(linear_search(SearchInput(buku, kunci)))
        print("[Binary Search]")
        cetak_hasil(binary_search(SearchInput(buku_urut, kunci)))


# =====================================================================
# BAGIAN 6.
# =====================================================================
def rata_waktu(fungsi, data_in) -> float:
    total = 0.0
    for _ in range(ULANG_WAKTU):
        total += fungsi(data_in).waktu_detik
    return total / ULANG_WAKTU


def pengujian(buku_utuh):
    posisi = [("awal", 0), ("tengah", None), ("akhir", None)]
    baris = []
    for n in UKURAN_INPUT:
        if n > len(buku_utuh):
            print(f"[dilewati] n={n} lebih besar dari jumlah data ({len(buku_utuh)})")
            continue
        subset = urutkan_judul(buku_utuh[:n])      # ambil n buku pertama, lalu urutkan
        kunci_uji = [
            ("awal", subset[0].judul),
            ("tengah", subset[(n - 1) // 2].judul),   # titik tengah pertama Binary Search
            ("akhir", subset[n - 1].judul),
            ("tidak ditemukan", "~~~ judul yang tidak ada ~~~"),
        ]
        for nama_algo, algo in [("Linear Search", linear_search), ("Binary Search", binary_search)]:
            for skenario, kunci in kunci_uji:
                data_in = SearchInput(subset, kunci)
                res = algo(data_in)
                if nama_algo == "Linear Search":
                    teori = n
                else:
                    teori = math.floor(math.log2(n)) + 1
                baris.append({
                    "n": n, "algoritma": nama_algo, "skenario": skenario,
                    "perbandingan": res.jumlah_perbandingan,
                    "waktu_us": rata_waktu(algo, data_in) * 1e6,
                    "teori_terburuk": teori,
                })
    return baris


def cetak_tabel(baris):
    print(f"\n{'n':>6} | {'Algoritma':<13} | {'Skenario':<16} | {'Perbandingan':>12} | {'Waktu (us)':>10} | {'Teori terburuk':>14}")
    print("-" * 88)
    for r in baris:
        print(f"{r['n']:>6} | {r['algoritma']:<13} | {r['skenario']:<16} | {r['perbandingan']:>12} | "
              f"{r['waktu_us']:>10.2f} | {r['teori_terburuk']:>14}")


def simpan_csv(baris, nama="hasil_pengujian.csv"):
    with open(nama, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(baris[0].keys()))
        w.writeheader()
        w.writerows(baris)
    print(f"\nTabel disimpan ke {nama}")


def buat_grafik(baris):
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Grafik dilewati. Pasang dulu dengan: pip install matplotlib")
        return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for algo, warna in [("Linear Search", "tab:red"), ("Binary Search", "tab:blue")]:
        ns, cmp_, wkt = [], [], []
        for n in UKURAN_INPUT:
            for r in baris:
                if r["n"] == n and r["algoritma"] == algo and r["skenario"] == "tidak ditemukan":
                    ns.append(n); cmp_.append(r["perbandingan"]); wkt.append(r["waktu_us"])
        ax[0].plot(ns, cmp_, "o-", color=warna, label=algo)
        ax[1].plot(ns, wkt, "o-", color=warna, label=algo)
    for a, judul, yl in [(ax[0], "Jumlah perbandingan (data tidak ditemukan)", "perbandingan"),
                         (ax[1], "Waktu eksekusi (data tidak ditemukan)", "mikrodetik")]:
        a.set_xscale("log"); a.set_yscale("log"); a.set_title(judul)
        a.set_xlabel("n (jumlah buku)"); a.set_ylabel(yl); a.legend(); a.grid(True, alpha=.3)
    plt.tight_layout()
    plt.savefig("grafik_pengujian.png", dpi=150)
    print("Grafik disimpan ke grafik_pengujian.png")


# =====================================================================
# PROGRAM UTAMA
# =====================================================================
def main():
    buku = baca_csv(NAMA_FILE_CSV)
    print(f"Data terbaca: {len(buku)} buku")

    buku_urut = urutkan_judul(buku)
    demo(buku, buku_urut)

    baris = pengujian(buku)
    cetak_tabel(baris)
    simpan_csv(baris)
    buat_grafik(baris)


if __name__ == "__main__":
    main()