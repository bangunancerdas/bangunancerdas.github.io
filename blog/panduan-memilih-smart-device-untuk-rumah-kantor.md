# Panduan Memilih Smart Device untuk Rumah/Kantor

> Panduan ini membantu memilih smart device dengan urutan yang masuk akal: tentukan tujuan yang bisa diukur, periksa apakah perangkat bergantung pada cloud, pastikan kompatibilitas, lalu nilai keamanan dan dukungan produsennya. Di akhir ada daftar periksa yang bisa dibawa saat membeli.

## 1. Tentukan masalah dan cara mengukurnya

Mulailah dari masalah, bukan perangkat: pencahayaan yang boros, AC yang menyala saat kosong, pintu yang sering lupa dikunci, atau konsumsi listrik yang tidak terlihat. Untuk setiap masalah, tulis ukuran keberhasilannya, misalnya kWh bulanan atau jumlah jam AC menyala di ruangan kosong. Tanpa ukuran, sulit menilai apakah perangkat itu layak dibeli. Untuk gambaran langkah-langkah penghematannya, baca [5 cara smart device menghemat tagihan listrik](/blog/5-cara-smart-device-menghemat-tagihan-listrik.html).

## 2. Periksa cara perangkat berkomunikasi: lokal atau cloud

Home Assistant mengelompokkan integrasi perangkat berdasarkan cara kerjanya. Pada integrasi lokal (*local push* atau *local polling*), perangkat berbicara langsung dengan hub di jaringan Anda. Pada integrasi cloud (*cloud push* atau *cloud polling*), komunikasi melalui server produsen dan memerlukan internet.[1] Perbedaan *push* dan *polling* ada pada kecepatan: pada *push* perangkat memberi tahu begitu ada perubahan, sedangkan pada *polling* hub bertanya secara berkala sehingga perubahan dapat terlambat terdeteksi.[1]

Konsekuensinya praktis. Integrasi cloud berhenti bekerja bila internet mati atau produsen menghentikan dukungan, dan mengandalkan cloud berarti menyerahkan sebagian kendali atas siapa yang dapat mengakses data Anda.[1] Tulisan itu berasal dari tahun 2016, tetapi pembedaan konsepnya masih relevan untuk menilai perangkat. Tanyakan sebelum membeli: apakah perangkat ini dapat dikontrol secara lokal tanpa akun cloud, dan apa yang terjadi bila server produsen tidak lagi tersedia?

## 3. Pastikan kompatibilitas

Matter adalah standar smart home dari Connectivity Standards Alliance yang bertujuan agar perangkat dari berbagai merek dapat bekerja bersama secara native dengan konektivitas lokal yang responsif. Rilis spesifikasi pertamanya berjalan di jaringan Wi-Fi dan Thread, dengan Bluetooth Low Energy untuk proses pemasangan.[2] Perangkat berlogo Matter memudahkan pencampuran merek, tetapi dukungan fitur dapat berbeda antarperangkat dan antarhub, jadi periksa daftar kompatibilitas pada hub atau aplikasi yang akan Anda pakai sebelum membeli dalam jumlah banyak.

## 4. Nilai keamanan dan dukungan produsen

ETSI EN 303 645 adalah standar Eropa tentang persyaratan dasar keamanan perangkat IoT konsumen, termasuk perangkat otomasi rumah dan hub-nya. Standar ini ditujukan bagi pihak yang mengembangkan dan memproduksi perangkat, tetapi ketentuannya berguna sebagai daftar pertanyaan bagi pembeli.[3] Beberapa di antaranya:

- **Kata sandi unik.** Kata sandi harus unik per perangkat atau ditentukan pengguna, bukan kata sandi bawaan yang sama untuk semua perangkat (ketentuan 5.1-1).[3]
- **Pelaporan celah keamanan.** Produsen wajib menyediakan kebijakan pengungkapan kerentanan secara publik (5.2-1).[3]
- **Masa dukungan pembaruan.** Produsen wajib mengumumkan secara jelas masa dukungan pembaruan perangkat lunaknya (5.3-13).[3]
- **Penghapusan data.** Pengguna harus dapat menghapus semua data pengguna dari perangkat dengan cara sederhana (5.11-1).[3]

Perangkat yang tidak mengumumkan masa dukungan atau tidak menyediakan cara menghapus data adalah tanda tanya. Ganti kata sandi bawaan, aktifkan pembaruan, dan pisahkan perangkat IoT dari jaringan kerja bila memungkinkan.

## 5. Perhatikan daya, instalasi, dan keselamatan

Catatan praktis (bukan kutipan sumber): perangkat yang dipasang pada instalasi listrik, seperti saklar pintar atau relay, sebaiknya dipasang teknisi listrik. Sebagian saklar pintar memerlukan kabel netral, dan setiap perangkat memiliki batas arus beban, jadi periksa spesifikasinya terhadap beban yang akan dikendalikan. Perangkat berbaterai seperti sensor membutuhkan penggantian baterai berkala.

## 6. Hitung biaya total

Biaya sesungguhnya mencakup perangkat, hub atau pengendali, pemasangan, langganan layanan cloud bila ada, penggantian baterai, dan waktu perawatan. Perangkat murah dengan dukungan produsen yang pendek dapat menjadi lebih mahal dalam jangka panjang.

> **Contoh ilustratif — bukan proyek nyata Bangunan Cerdas.**
>
> Sebuah rumah dengan tiga AC dan lampu teras ingin tahu AC mana yang boros. Pilihan yang masuk akal: satu meter energi yang dapat dibaca secara lokal, tiga colokan atau relay pengukur untuk AC, dan satu sensor kehadiran per ruangan. Sebelum membeli, pemilik memeriksa masa dukungan pembaruan, apakah perangkat bisa dikontrol tanpa cloud, dan apakah semuanya dapat dibaca satu hub. Contoh ini hanya ilustrasi proses pemilihan, bukan rekomendasi produk.

## Rumah atau kantor: apa bedanya

Kantor biasanya memiliki banyak pengguna sehingga perlu pembagian hak akses, jadwal yang mengikuti jam kerja dengan cara menimpa yang mudah, dan dokumentasi agar sistem tidak bergantung pada satu orang. Rumah lebih menekankan kemudahan dan privasi. Prinsip seleksinya sama, tetapi bobot tiap kriteria berbeda.

## Daftar periksa sebelum membeli

- Masalah dan ukuran keberhasilan sudah jelas tertulis.
- Perangkat dapat dikontrol secara lokal, atau ketergantungan cloud-nya sudah dipahami.
- Kompatibel dengan hub atau aplikasi yang akan dipakai (periksa Matter atau integrasi yang didukung).
- Kata sandi unik dan pembaruan keamanan tersedia.
- Masa dukungan pembaruan diumumkan produsen.
- Ada cara menghapus data dan menimpa otomasi secara manual.
- Spesifikasi listrik sesuai beban dan pemasangan dilakukan teknisi.
- Biaya total sudah dihitung.

## Referensi

1. Home Assistant (2016). [Classifying the Internet of Things](https://www.home-assistant.io/blog/2016/02/12/classifying-the-internet-of-things/). Tulisan blog, tanggal dari URL. Diakses 23 Oktober 2026.
2. Connectivity Standards Alliance. [Build With Matter | Smart Home Device Solution](https://csa-iot.org/all-solutions/matter/). Diakses 23 Oktober 2026.
3. ETSI (2024). [ETSI EN 303 645 V3.1.3: Cyber Security for Consumer Internet of Things: Baseline Requirements](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf). Standar Eropa, edisi September 2024. Diakses 23 Oktober 2026.
