# 5 Cara Smart Device Menghemat Tagihan Listrik

> Lima langkah konkret memakai smart device untuk mengurangi pemborosan listrik, lengkap dengan kondisi saat langkah itu efektif, risikonya, dan cara memeriksa hasilnya. Tidak ada angka penghematan universal, jadi artikel ini menunjukkan cara mengukurnya sendiri.

## Mulai dari daya dan energi

Dua istilah ini sering tertukar. **Daya** (watt, W) adalah besarnya listrik yang dipakai pada satu saat. **Energi** (kilowatt-jam, kWh) adalah daya dikalikan lamanya pemakaian. Penghematan terjadi ketika energi yang terpakai berkurang, entah karena dayanya lebih kecil atau karena perangkat menyala lebih singkat. Rincian tagihan listrik Anda tetap perlu diperiksa, karena komponen lain seperti daya tersambung dan tarif juga berpengaruh.

> **Contoh ilustratif — bukan proyek nyata Bangunan Cerdas.**
>
> Misalkan sebuah AC menarik daya 900 W (angka asumsi; periksa label perangkat atau ukur dengan meter). Menyala 8 jam, AC itu memakai 0,9 kW × 8 jam = 7,2 kWh. Jika AC yang sama menyala dua jam lebih lama di ruangan kosong, tambahan energinya 1,8 kWh. Itulah jenis pemborosan yang dapat ditangkap sensor.

## 1. Jadwalkan lampu sesuai jam aktivitas

Panduan FEMP (DOE Amerika Serikat) menyebut penjadwalan waktu sering efektif untuk area kantor terbuka yang luas dengan banyak penghuni, sedangkan sensor kehadiran lebih cocok untuk ruang yang kadang terpakai.[1] Di rumah, contohnya lampu teras yang menyala saat matahari terbenam, pemicu yang memang didukung aturan otomasi Home Assistant.[2]

Syaratnya, jadwal harus sesuai pola pemakaian dan penghuni harus bisa menimpanya dengan mudah, misalnya saat ada yang lembur.[1]

## 2. Matikan AC saat ruangan kosong dan jaga suhu wajar

Mematikan AC saat ruangan tidak digunakan adalah salah satu langkah dalam Peraturan Menteri ESDM Nomor 13 Tahun 2012, bersama penggunaan AC inverter dan pengaturan suhu ruang kerja pada kisaran 24 hingga 27 °C.[3] Aturan itu ditujukan bagi gedung negara dan sejenisnya, tetapi langkahnya masuk akal bagi siapa pun. Sensor kehadiran dan aturan batas suhu membuat langkah itu berjalan otomatis.

Hasilnya sangat bergantung pada pemasangan. Laporan PNNL tentang sensor kehadiran mencatat hasil dari tambahan penghematan 76 persen hingga hampir nol pada beberapa area parkir, dengan pesan bahwa desain, pemilihan, dan *commissioning* harus cermat.[4] FEMP menambahkan bahwa sensor harus menjangkau semua penghuni dan tidak terpapar lorong yang dilalui orang.[1] Tentukan jeda waktu (*delay*) yang cukup agar lampu atau AC tidak mati ketika orang hanya diam sebentar.

## 3. Pantau konsumsi per perangkat

Memantau saja sudah dapat mengubah perilaku. Tinjauan ACEEE atas program umpan balik energi di rumah tangga menemukan penghematan listrik rata-rata sekitar 4 hingga 12 persen pada 36 program yang dijalankan antara 1995 dan 2010, dan 2 hingga 11 persen bila hanya studi di Amerika Serikat yang dihitung.[5] Angka itu berasal dari program di luar Indonesia dan sangat bergantung pada rancangan programnya, jadi anggap sebagai gambaran kemungkinan, bukan janji.

Secara teknis, sensor daya dapat dikonversi menjadi data energi untuk dasbor, seperti pada dasbor energi Home Assistant yang melacak listrik jaringan, panel surya, baterai, dan perangkat individual.[6]

## 4. Kurangi beban puncak lewat skenario otomasi

Beban puncak terjadi ketika banyak perangkat berdaya besar menyala bersamaan, misalnya pemanas air, pompa, dan beberapa AC. Skenario otomasi dapat menggeser atau menyusun jadwal nyalanya. Manfaat finansialnya bergantung pada struktur tarif dan daya tersambung Anda, sehingga periksa rincian tagihan atau tanyakan ke penyedia listrik sebelum berharap pada penghematan biaya dari langkah ini.

## 5. Beri notifikasi saat konsumsi tidak wajar

Aturan otomasi dapat mengirim notifikasi sebagai aksinya.[2] Dengan data konsumsi, Anda dapat membuat peringatan ketika pemakaian jauh di atas kebiasaan, misalnya AC menyala semalaman atau pompa yang tidak berhenti. Kuncinya menetapkan batas dari data nyata beberapa minggu, bukan dari tebakan, supaya notifikasi tidak terlalu sering sehingga diabaikan.

## Seberapa besar penghematannya

Tidak ada satu angka yang berlaku untuk semua. Hasil bergantung pada kebiasaan penghuni, cuaca, jenis perangkat, dan mutu pemasangan, sebagaimana terlihat dari rentang temuan di atas.[5][4] Cara paling jujur adalah mengukur sendiri: catat konsumsi kWh sebelum perubahan, lalu bandingkan dengan periode sesudahnya yang kondisinya sebanding (jumlah hari kerja, cuaca, jumlah penghuni).

## Biaya dan hal yang sering terlewat

- Biaya total mencakup perangkat, pemasangan, dan perawatan (baterai sensor, pembaruan perangkat lunak), bukan hanya harga perangkat.
- Setiap perangkat pintar juga mengonsumsi daya kecil secara terus-menerus; periksa spesifikasinya.
- Perangkat terhubung perlu dijaga keamanannya; lihat [panduan memilih smart device](/blog/panduan-memilih-smart-device-untuk-rumah-kantor.html).
- Sediakan selalu cara manual untuk menimpa otomasi.

## Referensi

1. U.S. Department of Energy, Federal Energy Management Program (2000). [How to Select Lighting Controls for Offices and Public Buildings](https://www.energy.gov/sites/prod/files/2013/10/f3/light_controls.pdf). Lembar informasi LT-8, Desember 2000. Diakses 23 Oktober 2026.
2. Home Assistant. [Understanding automations](https://www.home-assistant.io/docs/automation/basics/). Diakses 23 Oktober 2026.
3. Menteri Energi dan Sumber Daya Mineral Republik Indonesia (2012). [Peraturan Menteri ESDM Nomor 13 Tahun 2012 tentang Penghematan Pemakaian Tenaga Listrik](https://jdih.esdm.go.id/storage/document/Permen%20ESDM%2013%202012.pdf). Ditetapkan 29 Mei 2012. Diakses 23 Oktober 2026.
4. Kinzey, B. R., Myer, M., Royer, M. P., dan Sullivan, G. P., Pacific Northwest National Laboratory (2012). [Use of Occupancy Sensors in LED Parking Lot and Garage Applications: Early Experiences](https://www.osti.gov/biblio/1057365). Laporan teknis PNNL-21923, 7 November 2012. Diakses 23 Oktober 2026.
5. Ehrhardt-Martinez, K., Donnelly, K. A., dan Laitner, J. A., American Council for an Energy-Efficient Economy (ACEEE) (2010). [Advanced Metering Initiatives and Residential Feedback Programs: A Meta-Review for Household Electricity-Saving Opportunities](https://www.aceee.org/research-report/e105). Laporan E105, Juni 2010. Diakses 23 Oktober 2026.
6. Home Assistant. [Home energy management](https://www.home-assistant.io/docs/energy/). Diakses 23 Oktober 2026.
