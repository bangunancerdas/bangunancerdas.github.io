# Bangunan Cerdas Website

Website profile statis untuk **Bangunan Cerdas** (Organization Site GitHub Pages):
https://bangunancerdas.github.io

## Struktur Folder

- `index.html` — halaman utama (home, tentang, manfaat, layanan, portfolio, blog, kontak)
- `styles.css` — styling responsive + theme variables (light/dark)
- `script.js` — dark/light toggle + localStorage + tahun footer
- `assets/logo/` — logo untuk header dan favicon
- `blog/` — artikel mini blog (`.html` untuk halaman publik, `.md` untuk draft/sumber konten)
- `.github/workflows/deploy.yml` — CI/CD deploy ke GitHub Pages
- `sitemap.xml` — sitemap URL website

## Cara Update Konten

### 1) Update nomor WhatsApp
Nomor saat ini: `+62 896-8085-8462` (link `wa.me` memakai format `6289680858462`).

### 2) Update isi halaman utama
Edit section terkait di `index.html`:
- Hero
- Tentang
- Manfaat
- Layanan
- Portfolio
- Kontak

### 3) Update artikel blog
- Tambah/edit halaman artikel di folder `blog/` (format `.html`)
- Tambahkan link artikel baru di section `#blog` pada `index.html`
- Tambahkan URL artikel baru ke `sitemap.xml`

### 4) Ganti foto placeholder portfolio dengan foto asli
Di section `#portfolio` pada `index.html`, ganti nilai `src` tiap `<img>` dengan file/foto asli.

Rekomendasi:
1. Simpan foto di `assets/images/portfolio/`
2. Kompres dulu (WebP/JPEG) sebelum upload
3. Pertahankan atribut `loading="lazy"`, `width`, `height`
4. Update `alt` agar deskriptif sesuai proyek

## Deploy GitHub Pages (Organization Site)

Workflow deploy otomatis jalan setiap push ke `main` via GitHub Actions.

Pastikan di GitHub repo settings:
- **Pages** → **Build and deployment**
- Source: **GitHub Actions**

Tidak perlu `CNAME` dan tidak perlu base path config karena ini organization site root.
