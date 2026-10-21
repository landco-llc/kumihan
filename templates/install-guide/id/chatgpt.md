Panduan ini menjelaskan cara menggunakan {{brand}} di ChatGPT dan Codex.

> **Tentang v{{version}}**
> Versi ini disediakan agar Anda dapat mencoba pemasangannya di lingkungan Anda sendiri. Cara kerjanya di setiap alat belum diuji secara menyeluruh, sehingga mungkin ada yang tidak berjalan sebagaimana mestinya.

## 1. Pilih cara pemasangan

| Tempat penggunaan | Cara yang disarankan |
| --- | --- |
| ChatGPT (jika tersedia unggahan skill) | [A. Tambahkan skill satu per satu](#a) |
| ChatGPT (sebagai plugin pribadi Anda sendiri) | [B. Daftarkan sekaligus sebagai plugin](#b) |
| Codex (di komputer Anda) | [C. Salin folder](#c) |

Satu **skill** berisi satu fungsi, sedangkan **plugin** adalah paket yang menggabungkan keempat skill.

## 2. Unduh berkas

Semua berkas tersedia di [halaman rilis]({{release}}). Klik tautan untuk mengunduh berkas ZIP.

**Plugin (gabungan keempat skill)**

- {{plugin_link}}

**Skill (satu per satu)**

{{skills_list}}

## A. Tambahkan skill ke ChatGPT

Cara ini dapat digunakan jika ChatGPT Anda menampilkan menu “Skills” beserta opsi unggah.

1. Pilih satu berkas ZIP skill, lalu unggah.
2. Periksa keterangan yang ditampilkan, lalu tambahkan.
3. Ulangi langkah yang sama untuk setiap skill yang Anda perlukan.

**Catatan**

- ZIP plugin tidak dapat digunakan dengan cara ini. Gunakan ZIP skill.
- Melampirkan berkas ke percakapan saja tidak menambahkannya sebagai skill.
- Jika Anda tidak menemukan opsinya, fitur ini mungkin belum tersedia untuk paket langganan atau aplikasi Anda. Lihat [panduan resmi OpenAI](https://learn.chatgpt.com/docs/build-skills).

## B. Daftarkan sebagai plugin di ChatGPT

Cara ini mendaftarkan keempat skill sekaligus sebagai plugin pribadi Anda sendiri.

1. Buka percakapan baru di ChatGPT, lalu pilih `@plugin-creator`.
2. Lampirkan berkas ZIP plugin.
3. Mintalah seperti berikut:

   > Tolong daftarkan paket ini sebagai plugin pribadi saya. Jangan ajukan ke direktori publik.

4. Setelah terdaftar, **{{display}}** akan muncul di Plugins, pada “Personal” atau “Created by me”.
5. Pasang jika perlu, lalu aktifkan di percakapan baru.

**Catatan**

- Plugin bisa saja tersimpan di ruang kerja (workspace) tim Anda. Jika ingin hanya untuk Anda sendiri, periksa lokasi penyimpanannya sebelum mendaftarkan.
- Fitur ini mungkin tidak tersedia, tergantung pada paket langganan atau pengaturan ruang kerja Anda. Lihat [Build plugins](https://learn.chatgpt.com/docs/build-plugins) dan [Plugins](https://learn.chatgpt.com/docs/plugins).
- Plugin yang didaftarkan dengan cara ini hanya dapat digunakan di akun Anda. Plugin ini tidak dimuat di direktori publik.

## C. Salin folder untuk Codex

Mengekstrak ZIP skill akan menghasilkan folder seperti `{{first}}`. Salin folder tersebut ke lokasi tempat Codex membaca skill.

| Cakupan penggunaan | Lokasi tujuan |
| --- | --- |
| Hanya di proyek tertentu | `.agents/skills/` di dalam proyek |
| Di semua proyek | `~/.agents/skills/` di folder beranda (home) |

Misalnya, untuk menambahkan `{{first}}` ke sebuah proyek:

```sh
mkdir -p /path/to/your-project/.agents/skills
cp -R {{first}} /path/to/your-project/.agents/skills/
```

**Catatan**

- Salin folder secara utuh beserta seluruh isinya. Skill tidak akan berjalan dengan benar jika hanya sebagian berkas yang disalin.
- Jika sudah ada folder dengan nama yang sama, periksa isinya sebelum menimpanya.

## 3. Coba gunakan

Setelah terpasang, buka percakapan baru dan panggil skill.

| Alat | Cara memanggil |
| --- | --- |
| ChatGPT | Pilih dari `@` |
| Codex | Pilih dari `$` atau `/skills` |

Sebaiknya mulai dengan permintaan yang tidak mengubah berkas apa pun:

> Saya berencana membuat laporan dalam bahasa Indonesia. Hal apa saja yang perlu saya perhatikan? Tolong jangan ubah berkas apa pun.

## Periksa keutuhan berkas (opsional)

Jika ingin memastikan berkas yang diunduh tidak rusak, gunakan [SHA256SUMS.txt]({{sums}}).

Letakkan SHA256SUMS.txt di folder yang sama dengan berkas ZIP yang diunduh, lalu jalankan perintah berikut di terminal. Jika `shasum` tidak tersedia, cocokkan nilai SHA-256 dengan cara lain, misalnya `Get-FileHash` di Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jika baris untuk berkas yang Anda unduh menampilkan `OK`, berkas tersebut aman.

---

Alat lain: [Claude]({{page_claude}}) · [Gemini]({{page_gemini}})

Tampilan dan ketentuan layanan dapat berubah. Untuk informasi terbaru, silakan periksa panduan resmi setiap layanan (halaman ini terakhir diperiksa pada 14 Oktober 2026).
