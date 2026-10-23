# Bangunan Cerdas — Company Profile Website

Website company profile statis untuk **Bangunan Cerdas**, berfokus pada solusi **smart building** dan **smart home** dengan orientasi efisiensi energi.

**Production URL:** https://bangunancerdas.github.io

## Ringkasan

Project ini dibangun sebagai static site ringan berbasis HTML/CSS/JavaScript tanpa framework berat, dengan fokus:

- performa loading cepat,
- desain responsif (mobile-first),
- dark/light theme toggle dengan persistensi preferensi pengguna,
- deployment otomatis ke GitHub Pages via GitHub Actions.

## Fitur Utama

- Landing page lengkap: Hero, Tentang, Manfaat, Layanan, Portfolio (skenario konsep, bukan proyek klien), Blog, Kontak
- Dark/Light mode:
  - auto-detect `prefers-color-scheme`,
  - manual override via toggle,
  - preferensi disimpan di `localStorage`,
  - early theme script di `<head>` untuk mencegah flash tema yang salah
- Mini blog dengan halaman artikel terpisah (`/blog/*.html`)
- SEO baseline:
  - meta description,
  - Open Graph,
  - canonical URL di setiap halaman,
  - structured data `schema.org` (`LocalBusiness` di beranda, `BlogPosting` di artikel),
  - `sitemap.xml` dan `robots.txt`
- Kontak WhatsApp kontekstual (pesan berbeda per CTA) dan tracking konversi opsional yang **nonaktif secara default** (lihat bagian Analytics)
- GitHub Pages CI/CD modern:
  - job `quality` (tes otomatis) harus lulus sebelum job `deploy`
  - `actions/upload-pages-artifact`
  - `actions/deploy-pages`

## Teknologi

- HTML5
- CSS3 (custom properties / CSS variables)
- Vanilla JavaScript
- GitHub Actions (quality checks + Pages deployment)
- Tooling pengembangan (tidak ikut dipublikasikan): Python 3 (`unittest`), Node.js (`node --test`), Java + Nu HTML Checker

## Struktur Repository

```text
.
├── .github/workflows/deploy.yml   # quality -> deploy
├── 404.html
├── analytics.js                   # analytics opsional (nonaktif default)
├── assets/
│   ├── og-image.png               # gambar pratinjau sosial 1200x630
│   └── logo/
├── blog/
│   ├── *.html
│   └── *.md                       # draft, tidak ditautkan dan tidak masuk sitemap
├── index.html
├── robots.txt
├── scripts/                       # check.sh, validate-html.sh
├── script.js                      # toggle tema + tahun footer
├── sitemap.xml
├── styles.css
└── tests/                         # tes Python (statis) dan tests/js (perilaku JS)
```

## Menjalankan Secara Lokal

Gunakan static server sederhana:

```bash
python3 -m http.server 8080
```

Akses di: `http://localhost:8080`

## Quality Checks

Jalankan semua pemeriksaan yang sama dengan CI:

```bash
./scripts/check.sh
```

Skrip ini menjalankan:

1. `python3 -m unittest discover -s tests -t . -v`: tautan internal & fragment, aset lokal, placeholder portfolio, metadata SEO, canonical, JSON-LD, sitemap, URL WhatsApp, struktur HTML.
2. `node --test tests/js`: inisialisasi & persistensi tema, perilaku analytics.
3. `./scripts/validate-html.sh`: validasi HTML dengan Nu HTML Checker (butuh Java dan npm; jar `vnu-jar` diunduh sekali ke direktori cache sementara).

Yang **tidak** dicakup tes otomatis ini: tampilan visual dan responsif (lihat daftar viewport di bawah), pengukuran Core Web Vitals, serta pengiriman data analytics ke provider. Pemeriksaan tersebut dilakukan manual (mis. Lighthouse atau DevTools). Viewport yang disarankan: 320×568, 375×812, 390×844, 768×1024, 1024×768, 1440×900.

## Deployment

Setiap push ke branch `main` menjalankan job `quality`; job `deploy` ke GitHub Pages hanya berjalan jika job tersebut lulus. Pull request hanya menjalankan `quality`. Folder `tests/`, `scripts/`, `.github/` dan `README.md` tidak ikut dipublikasikan.

Prasyarat di GitHub repository settings:

1. **Settings → Pages**
2. **Build and deployment → Source: GitHub Actions**

Karena ini **Organization Site** (`bangunancerdas.github.io`), tidak memerlukan `CNAME` maupun base path khusus.

## Panduan Maintenance Konten

### 1. Update nomor WhatsApp

Nomor aktif saat ini:

- Display: `+62 896-8085-8462`
- Link format: `https://wa.me/6289680858462`

Nomor muncul di beberapa halaman (semua link `wa.me`, teks di bagian Kontak, dan `telephone` di JSON-LD). Format `wa.me` harus tanpa tanda `+`, spasi, atau dash.

Aturan CTA WhatsApp (dijaga oleh `tests/test_whatsapp.py`):

- Setiap link memakai pesan Indonesia yang sesuai konteks dan di-encode dengan benar (`text=` dengan percent-encoding, spasi `%20`).
- Wajib ada `data-track` (`whatsapp_click`, `service_cta_click`, atau `portfolio_click`) dan `data-cta-id` yang unik per halaman (huruf kecil, angka, tanda hubung).
- Wajib `target="_blank" rel="noopener noreferrer"` dan teks/`aria-label` yang menyebut WhatsApp.
- Jika nomor diganti, ubah `WHATSAPP_NUMBER` di `tests/site.py` bersama semua link, teks Kontak, dan JSON-LD.

### 2. Update konten halaman utama

Edit langsung di `index.html` pada section terkait:

- Hero
- Tentang
- Manfaat
- Layanan
- Portfolio
- Blog list
- Kontak

### 3. Update/tambah artikel blog

1. Tambah file artikel baru di `blog/` dengan format `.html`
2. Tambahkan link artikel di section Blog pada `index.html`
3. Tambahkan URL artikel baru ke `sitemap.xml`

Setiap artikel memerlukan: `<link rel="canonical">`, Open Graph lengkap, JSON-LD `BlogPosting` (tanpa tanggal/penulis yang tidak terverifikasi), bagian "Baca juga" (minimal dua artikel lain), tautan ke `/#layanan`, dan CTA WhatsApp dengan judul artikel pada pesannya. Tes akan gagal jika ada yang kurang. Judul pada `.md` harus sama dengan `<h1>` di `.html`.

File `.md` di folder `blog/` dapat dipakai sebagai draft/internal source, namun halaman publik menggunakan `.html`.

## Analytics (opsional, nonaktif)

`analytics.js` mendukung event `whatsapp_click`, `service_cta_click`, `portfolio_click`, dan `article_read` lewat [GoatCounter](https://www.goatcounter.com/) (tanpa cookie). **Tidak ada data yang dikirim** sampai semua langkah ini selesai:

1. Buat akun GoatCounter dan catat kode situs (subdomain `<kode>.goatcounter.com`).
2. Tinjau praktik data provider dan kebutuhan persetujuan/pemberitahuan privasi (UU PDP Indonesia serta yurisdiksi pengunjung). Repository ini tidak berisi kebijakan privasi dan tidak menjamin kepatuhan hukum; tinjauan hukum diperlukan.
3. Di `analytics.js`, ubah `CONFIG.enabled` menjadi `true` dan isi `CONFIG.goatcounterCode`.

Perilaku yang dijaga tes: event hanya berisi nama event, ID CTA, dan path halaman (tanpa nomor telepon, isi pesan, query string, atau hash); Do Not Track dan Global Privacy Control menonaktifkan tracking; kegagalan provider tidak mengganggu halaman; link WhatsApp tetap berfungsi tanpa JavaScript. `article_read` terkirim sekali setelah akhir artikel terlihat dan tab terlihat minimal 15 detik.

Belum diverifikasi: pengiriman data nyata ke GoatCounter (tidak ada akun/kode situs).

### 4. Portfolio

Saat ini belum ada dokumentasi proyek klien yang dapat dipublikasikan, sehingga section `#portfolio` menampilkan **skenario konsep** yang diberi label jelas ("Skenario konsep"), tanpa klaim hasil. Jangan menambahkan proyek, klien, atau angka penghematan yang tidak dapat dibuktikan.

Setiap `.portfolio-item` wajib punya `data-kind`:

- `concept`: label "konsep" terlihat, tanpa `<img>` dan tanpa elemen `.result`.
- `project`: proyek nyata. Wajib ada `<img>` lokal (file harus ada) dengan `alt` deskriptif, `width`, dan `height`. Simpan gambar di `assets/images/portfolio/`, kompres (WebP/JPEG), pakai `loading="lazy"`, dan pastikan Anda berhak mempublikasikannya (izin klien).

Gambar dari host eksternal/placeholder (mis. Unsplash) ditolak oleh tes.
