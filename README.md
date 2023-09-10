# MST-Finder
MST-Finder merupakan program berbasis GUI yang mencari Minimum Spanning Tree (MST) dari suatu graf. Pencarian MST dilakukan menggunakan algoritma prim dan algoritma kruskal. MST-Finder juga dapat melakukan clustering berdasarkan MST yang ditemukan.


# Requirements
1. Python 3
2. NetworkX
3. Matplotlib


# How To use
Untuk menjalankan program, pengguna cukup menjalankan ```Main.py``` pada folder ```src``` salah satu caranya bisa dengan mengetikkan ```python Main.py``` pada directory ```Main.py``` berada. Setelah itu, akan muncul sebuah GUI seperti berikut:

![image](docs/image.png?raw=true)


Untuk membaca file txt graf, pengguna dapat mengeklik tombol Open File pada bagian bawah kiri, setelah itu akan muncul halaman memilih file.

![image](docs/image1.png?raw=true)

Silahkan pilih file txt berisikan graf, lalu klik tombol open. Setelah itu, graf akan langsung divisualisasi

![image](docs/image2.png?raw=true)

Untuk mencari MST, pengguna dapat memilih algoritma yang ingin digunakan pada bagian kanan atas. Setelah memilih algoritma, klik tombol Solve. Hasil MST-pun akan langsung divisualisasikan.

![image](docs/image3.png?raw=true)

Untuk mengembalikan tampilan graf yang asli dapat menekan tombol Reset.

![image](docs/image4.png?raw=true)

Pengguna juga dapat merename node dengan mengeklik tombol Rename Node pada bagian kanan bawah. Halaman Rename akan muncul dan pengguna dapat mengganti nama node di halaman tersebut (Field Old Name berisikan nama node yang ingin diganti, sedangkan field New Name berisikan nama node yang baru).

![image](docs/image5.png?raw=true)

![image](docs/image6.png?raw=true)

Pengguna juga dapat menambah node/edge dengan mengeklik tombol Add Node/Edge. Halaman Add Node/Edge akan muncul. Di sini pengguna dapat menambah node atau edge (Untuk menambah node, cukup isi field Node dan klik tombol Add Node. Sedangkan, untuk menambah edge pengguna harus mengisi field Node 1, Node 2, dan Weight lalu klik tombol Add Edge).

![image](docs/image7.png?raw=true)

![image](docs/image8.png?raw=true)

Pengguna juga dapat menghapus node/edge dengan mengeklik tombol Delete Node/Edge. Halaman Delete Node/Edge akan muncul. Di sini pengguna dapat menghapus node atau edge (Untuk menghapus node, cukup isi field Node dan klik tombol Delete Node. Sedangkan, untuk menghapus edge pengguna harus mengisi field Node 1, Node 2, dan Weight lalu klik tombol Delete Edge).

![image](docs/image9.png?raw=true)

![image](docs/image10.png?raw=true)

Pengguna dapat melakukan clustering berdasarkan MST. Untuk melakukan clustering pengguna perlu mencari MST terlebih dahulu lalu mengisi field N dan klik tombol Search.

![image](docs/image11.png?raw=true)


# Author
Muhammad Equilibrie Fajria (13521047)
