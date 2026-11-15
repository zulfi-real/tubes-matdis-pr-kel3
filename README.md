Latar Belakang

Pada 16-18 April 2025, meningkatnya aktivitas bongkar muat di Pelabuhan Tanjung Priok menyebabkan antrean truk mengular di jalan akses dan jalan tol sekitarnya. Dampaknya meluas sampai ambulans ikut terjebak, dan seorang petugas medis terpaksa mendorong pasien sejauh 500-700 meter ke RSUD Koja.

Skenario kasus mengacu pada liputan KOMPAS TV: Ambulans Terjebak Macet, Inilah Cerita Petugas Medis Dorong Pasien di Tengah Macet Priok.

Tujuan
Merepresentasikan jaringan jalan sebagai graph (node = titik/lokasi, edge = ruas jalan).
Menganalisis kapasitas dan arus pada jaringan tersebut dengan graph algorithms.
Membandingkan beberapa skenario kebijakan, misalnya penambahan jalan, perubahan kapasitas gerbang, penutupan jalan, dan contraflow.
Meninjau arus kendaraan darurat (ambulans) menuju rumah sakit.
Pendekatan

Kasus dimodelkan dalam dua model (Model A dan Model B) yang didefinisikan di file konfigurasi YAML berisi node, edge (dengan atribut seperti jarak dan kapasitas), rencana eksekusi, dan daftar event/skenario. Program membaca file tersebut, membangun graph, lalu menjalankan algoritma yang dipilih.

Algoritma yang digunakan:

Maximum flow: Ford-Fulkerson (adaptasi dari template), Dinic, dan Push-Relabel, untuk menghitung arus maksimum dari sumber ke tujuan.
Minimum Spanning Tree (MST): berdasarkan jarak antar node.
Sumber Data dan Asumsi
Sebagian angka diambil dari pemberitaan (misalnya volume truk saat kejadian dan rata-rata harian normal).
Angka lain (kapasitas dan jarak ruas jalan) merupakan asumsi ilustratif dan perlu diganti dengan data resmi (PKJI / HCM / Dishub / Jasa Marga) sebelum dipakai dalam laporan.

Hasil dari project ini bersifat ilustratif untuk keperluan pembelajaran, bukan prediksi lalu lintas yang sebenarnya.

Referensi
KOMPAS TV, "Ambulans Terjebak Macet, Inilah Cerita Petugas Medis Dorong Pasien di Tengah Macet Priok", 19 April 2025. https://www.youtube.com/watch?v=teeHTybXUEc
