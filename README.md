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

- Landing page lengkap: Hero, Tentang, Manfaat, Layanan, Portfolio, Blog, Kontak
- Dark/Light mode:
  - auto-detect `prefers-color-scheme`,
  - manual override via toggle,
  - preferensi disimpan di `localStorage`,
  - early theme script di `<head>` untuk mencegah flash tema yang salah
- Mini blog dengan halaman artikel terpisah (`/blog/*.html`)
- SEO baseline:
  - meta description,
  - Open Graph,
  - structured data `schema.org` (`LocalBusiness`),
  - `sitemap.xml`
- GitHub Pages CI/CD modern:
  - `actions/upload-pages-artifact`
  - `actions/deploy-pages`

## Teknologi

- HTML5
- CSS3 (custom properties / CSS variables)
- Vanilla JavaScript
- GitHub Actions (Pages deployment)

## Struktur Repository

```text
.
├── .github/workflows/deploy.yml
├── 404.html
├── assets/
│   ├── images/
│   └── logo/
├── blog/
│   ├── *.html
│   └── *.md
├── index.html
├── script.js
├── sitemap.xml
└── styles.css
```

## Menjalankan Secara Lokal

Gunakan static server sederhana:

```bash
cd /home/justsomeone/Git/bangunancerdas.github.io
python3 -m http.server 8080
```

Akses di: `http://localhost:8080`

## Deployment

Setiap push ke branch `main` akan memicu workflow deploy ke GitHub Pages.

Prasyarat di GitHub repository settings:

1. **Settings → Pages**
2. **Build and deployment → Source: GitHub Actions**

Karena ini **Organization Site** (`bangunancerdas.github.io`), tidak memerlukan `CNAME` maupun base path khusus.

## Panduan Maintenance Konten

### 1. Update nomor WhatsApp

Nomor aktif saat ini:

- Display: `+62 896-8085-8462`
- Link format: `https://wa.me/6289680858462`

Jika mengubah nomor, pastikan format `wa.me` tetap tanpa tanda `+`, spasi, atau dash.

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

File `.md` di folder `blog/` dapat dipakai sebagai draft/internal source, namun halaman publik menggunakan `.html`.

### 4. Ganti foto placeholder portfolio

Di `index.html` (section `#portfolio`):

1. Ganti URL `src` image placeholder dengan aset asli
2. Simpan file gambar di `assets/images/portfolio/` (disarankan)
3. Kompres gambar (WebP/JPEG) sebelum dipakai
4. Pertahankan atribut `loading="lazy"`, `width`, `height`
5. Sesuaikan teks `alt` agar deskriptif dan relevan
