# QA Report — SAWIT PANIC! v5.7 Creator Credit

**Tanggal:** 22 Oktober 2026  
**Source:** v5.6 Progressive Difficulty & Bonus Harvest  
**Scope:** penambahan Premium Creator Signature di Main Menu

## Hasil LULUS

1. Nama tampil persis `DEVELOPED BY` dan `nugrohoiif` di Main Menu.
2. Credit non-interaktif (`pointer-events:none`) dan memiliki label aksesibilitas.
3. Tidak bertabrakan secara geometris dengan area sentuh `MAIN SEKARANG`, `TUTORIAL`, `PAPAN SKOR`, `PENGATURAN`, `SOUND`, Settings ikon kanan atas, atau badge rekor.
4. Nameplate tetap di dalam panggung virtual 540×960, dengan FIT scaling yang mempertahankan aspek 9:16.
5. Uji pada viewport **360×640, 375×667, 390×844, 412×915, 540×960**.
6. Semua tujuh tombol Main Menu tetap merespons dalam pengujian Chromium.
7. Tombol Main Sekarang berpindah ke layar gameplay; tombol-tombol modal membuka dialog; Sound tidak memicu error.
8. `prefers-reduced-motion: reduce` mematikan animasi signature.
9. Tidak ada JavaScript `pageerror` dalam semua skenario.
10. Validasi dif sumber: setelah mengeluarkan markup dan style credit serta pembaruan judul halaman, **source v5.7 identik byte-per-byte dengan v5.6**.

## Preview
- `menu-540x960.png` — resolusi virtual asli.
- `menu-390x844.png` — viewport mobile portrait.
- Screenshot viewport tambahan untuk pemeriksaan clipping.

## Belum diuji
- Perangkat iPhone/Android fisik, performa di GPU mobile, variasi rendering font lintas OS.
- Pengujian regresi end-to-end pada semua mekanik permainan; validasi regresi terutama melalui pemeriksaan source yang tidak berubah dan uji tombol Main Menu.

## Komponen yang ditambahkan
- `#menuCreatorCredit` di section `#menu`
- CSS `.creator-credit`, `.creator-credit-label`, `.creator-credit-name` dan keyframes, dengan reduced-motion fallback
- Tidak ada handler JavaScript atau state baru.
