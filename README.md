# SAWIT PANIC! v5.7 — Creator Credit Fix

## Perbaikan
Credit kreator yang disetujui kini BENAR-BENAR terlihat pada Main Menu:

- `DEVELOPED BY`
- `nugrohoiif` (huruf kecil persis sesuai permintaan)

Lokasi: footer tengah, di bawah tiga tombol utama. Credit bersifat **non-interaktif** agar tidak menciptakan false affordance. Tampilan berupa nameplate hijau tropis berbingkai emas, dengan animasi masuk fade/slide 450 ms dan satu shimmer ringan. Bila `prefers-reduced-motion` aktif, animasi dinonaktifkan.

## Batas perubahan
Game berasal dari v5.6. **Tidak ada perubahan** pada gambar logo, SawitMan, posisi tombol, artwork menu, skor, tiga hati, Bonus Harvest, musik, Pause Menu, atau gameplay. Semua fitur awal sudah ada pada satu file `index.html`.

## Cara menjalankan
Buka `index.html` di browser modern. Bila ingin membagikan atau meng-hosting, unggah file tersebut dan gunakan HTTPS. File berisi semua gambar dan kode secara embedded.

## Verifikasi
Lihat `QA_REPORT.md` dan folder preview `menu-*.png`. Pengujian dilakukan dengan Chromium terotomasi, bukan perangkat mobile fisik.
