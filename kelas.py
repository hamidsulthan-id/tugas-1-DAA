import csv
from dataclasses import dataclass
from typing import List, Optional


# =====================================================================
# BAGIAN 1. KELAS INPUT DAN OUTPUT  
# =====================================================================
@dataclass
class Buku:                       
    judul: str                    
    judul_kunci: str              
    penulis: str = "-"
    kategori: str = "-"
    rating: Optional[float] = None
    harga: Optional[float] = None


@dataclass
class SearchInput:                
    dataset: List[Buku]
    keyword: str


@dataclass
class SearchResult:               
    ditemukan: bool
    buku: Optional[Buku]
    indeks: int
    jumlah_perbandingan: int
    waktu_detik: float


# =====================================================================
# BAGIAN 2. MEMBACA DATASET DARI CSV
# =====================================================================
def ke_angka(teks):
    """Ubah teks jadi angka desimal, kosong jadi None."""
    bersih = "".join(c for c in (teks or "") if c.isdigit() or c in ".-")
    try:
        return float(bersih)
    except ValueError:
        return None


def baca_csv(nama_file) -> List[Buku]:
    hasil = []
    with open(nama_file, newline="", encoding="utf-8", errors="replace") as f:
        for baris in csv.DictReader(f):
            judul = (baris.get("title") or "").strip()
            if judul == "":
                continue
            hasil.append(Buku(
                judul=judul,
                judul_kunci=judul.lower(),
                penulis=(baris.get("authors") or "-").strip(),
                kategori=(baris.get("categories") or "-").strip(),
                rating=ke_angka(baris.get("average_rating")),
                harga=ke_angka(baris.get("list_price")),
            ))
    return hasil


def urutkan_judul(buku: List[Buku]) -> List[Buku]:
    """Urutkan abjad berdasarkan judul (syarat Binary Search)."""
    return sorted(buku, key=lambda b: b.judul_kunci)