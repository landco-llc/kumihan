Panduan ini menjelaskan cara menggunakan {{brand}} di Gemini CLI dan aplikasi Gemini.

> **Tentang v{{version}}**
> Versi ini disediakan agar Anda dapat mencoba pemasangannya di lingkungan Anda sendiri. Cara kerjanya di setiap alat belum diuji secara menyeluruh, sehingga mungkin ada yang tidak berjalan sebagaimana mestinya.

## 1. Pilih cara pemasangan

| Tempat penggunaan | Cara yang disarankan |
| --- | --- |
| Gemini CLI (keempatnya sekaligus) | [A. Pasang sebagai ekstensi](#a) |
| Gemini CLI (hanya yang diperlukan) | [B. Pilih dan pasang skill](#b) |
| Aplikasi Gemini (web, Mac, ponsel) | [C. Unggah skill](#c) |

## A. Gemini CLI: pasang sebagai ekstensi

Cara ini memasang keempat skill sekaligus.

1. Unduh [ZIP ekstensi]({{plugin_url}}).
{{#if plugin_folder}}
2. Ekstrak ZIP tersebut untuk mendapatkan folder `{{plugin_folder}}`.
{{else}}
2. Buat folder `{{plugin}}` yang kosong, lalu ekstrak ZIP ke dalamnya.
{{/if}}
3. Pasang dengan menunjuk folder tersebut:

   ```sh
   gemini extensions install "/absolute/path/{{plugin_dir}}"
   ```

Jika muncul layar konfirmasi, periksa isinya sebelum melanjutkan. Setelah dipasang, ekstensi aktif di semua proyek.

Ekstensi yang dipasang dari ZIP tidak diperbarui secara otomatis. Jika versi baru dirilis, ganti dengan ZIP yang baru.

## B. Gemini CLI: pilih dan pasang skill

Cara ini memasang hanya skill yang diperlukan, per proyek. Jika Anda sudah memakai cara A, langkah ini tidak diperlukan.

Misalnya, untuk memasang `{{first}}`, jalankan perintah berikut di proyek yang dituju:

```sh
gemini skills install https://github.com/landco-llc/kumihan --path {{skills_path}}/{{first}} --scope workspace
```

Untuk memasang skill lain, ubah `--path` seperti berikut:

{{gemini_paths}}

`--scope workspace` membatasi skill hanya untuk proyek ini. Jika dihilangkan, skill dapat digunakan di semua proyek Anda.

**Cara memperbarui**

Jalankan perintah yang sama sekali lagi. Skill yang sudah terpasang akan diganti, jadi simpan terlebih dahulu perubahan yang pernah Anda buat.

## C. Aplikasi Gemini: unggah skill

1. Unduh ZIP skill yang ingin Anda gunakan.
{{skills_list_indented}}
2. Di Gemini, buka **Customize** (jika tidak terlihat, **More**) → **Skills** → **Upload**.
3. Pilih ZIP satu per satu, periksa isinya, lalu tekan **Create**.

**Catatan**

- Fitur ini tersedia untuk akun Google pribadi milik pengguna berusia 18 tahun ke atas. Akun kerja dan akun sekolah saat ini belum didukung.
- “Keep Activity” (Simpan Aktivitas) harus diaktifkan.
- Fitur ini diluncurkan secara bertahap, sehingga mungkin belum muncul di akun Anda. Lihat [Bantuan resmi Gemini](https://support.google.com/gemini/answer/17094296?hl=id).
- ZIP ekstensi (untuk Gemini CLI) tidak dapat digunakan di sini.
- Skill yang diunggah tidak diperbarui secara otomatis. Jika versi baru dirilis, unggah kembali.

## 2. Coba gunakan

Sebaiknya mulai dengan permintaan yang tidak mengubah berkas apa pun:

> Saya berencana membuat materi presentasi dalam bahasa Indonesia. Hal apa saja yang perlu saya perhatikan? Tolong jangan ubah berkas apa pun.

## Periksa keutuhan berkas (opsional)

Jika ingin memastikan berkas yang diunduh tidak rusak, gunakan [SHA256SUMS.txt]({{sums}}).

Letakkan SHA256SUMS.txt di folder yang sama dengan berkas ZIP yang diunduh, lalu jalankan perintah berikut di terminal. Jika `shasum` tidak tersedia, cocokkan nilai SHA-256 dengan cara lain, misalnya `Get-FileHash` di Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jika baris untuk berkas yang Anda unduh menampilkan `OK`, berkas tersebut aman.

---

Alat lain: [ChatGPT / Codex]({{page_chatgpt}}) · [Claude]({{page_claude}})

Tampilan dan ketentuan layanan dapat berubah. Untuk informasi terbaru, silakan periksa panduan resmi setiap layanan (halaman ini terakhir diperiksa pada 14 Oktober 2026).
