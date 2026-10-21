Panduan ini menjelaskan cara menggunakan {{brand}} di Claude Code dan chat Claude.

> **Tentang v{{version}}**
> Versi ini disediakan agar Anda dapat mencoba pemasangannya di lingkungan Anda sendiri. Cara kerjanya di setiap alat belum diuji secara menyeluruh, sehingga mungkin ada yang tidak berjalan sebagaimana mestinya.

## 1. Pilih cara pemasangan

| Tempat penggunaan | Cara yang disarankan |
| --- | --- |
{{#if marketplace}}
| Claude Code | [A. Pasang dari GitHub](#a) (mudah diperbarui) |
{{/if}}
| Claude Code (jika ingin memasang dari ZIP) | [{{L_zip}}. Pasang dari ZIP](#{{l_zip}}) |
| Chat Claude (claude.ai dan aplikasi) | [{{L_chat}}. Unggah skill](#{{l_chat}}) |

Claude Code dan chat Claude dipasang dengan cara yang berbeda.

{{#if marketplace}}
## A. Claude Code: pasang dari GitHub

1. Di terminal, daftarkan sumber distribusi KUMIHAN.

   ```sh
   claude plugin marketplace add "https://github.com/landco-llc/kumihan.git#main"
   ```

2. Dalam percakapan Claude Code, ketik perintah berikut:

   ```text
   /plugin install {{plugin}}@kumihan-marketplace
   ```

3. Periksa keterangannya, pilih cakupan penggunaan (hanya untuk Anda, hanya untuk proyek ini, dan sebagainya), lalu pasang.

Setelah terpasang, perintah berikut dapat digunakan:

{{claude_commands}}

{{/if}}
## {{L_zip}}. Claude Code: pasang dari ZIP

1. Unduh [ZIP plugin untuk Claude Code]({{plugin_url}}).
{{#if plugin_folder}}
2. Ekstrak ZIP tersebut untuk mendapatkan folder `{{plugin_folder}}`.
{{else}}
2. Buat folder `{{plugin}}` yang kosong, lalu ekstrak ZIP ke dalamnya.
{{/if}}
3. Jalankan Claude Code dengan menunjuk folder tersebut:

   ```sh
   claude --plugin-dir "/absolute/path/{{plugin_dir}}"
   ```

**Catatan**

- Gunakan isi folder apa adanya. Jangan menghapus berkas atau mencampurnya dengan berkas lain.
- Dengan cara ini, pembaruan tidak berlangsung otomatis. Jika versi baru dirilis, ganti folder dengan isi ZIP yang baru.

## {{L_chat}}. Chat Claude: unggah skill

Cara ini untuk claude.ai dan aplikasi Claude.

1. Unduh ZIP skill yang ingin Anda gunakan.
{{skills_list_indented}}
2. Di Claude, buka **Customize → Skills**, lalu pilih **Upload a skill** dari tombol tambah.
3. Unggah ZIP satu per satu, lalu aktifkan setiap skill.

**Catatan**

- ZIP plugin untuk Claude Code tidak dapat digunakan di sini. Gunakan ZIP skill.
- Unggah ZIP tanpa mengubah nama berkasnya.
- Untuk menggunakan skill, eksekusi kode harus diaktifkan di pengaturan. Lihat [panduan resmi Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).
- Pada akun organisasi, fitur ini mungkin tidak tersedia, tergantung pada pengaturan administrator.
- Skill yang diunggah tidak diperbarui secara otomatis. Jika versi baru dirilis, unggah kembali.

## 2. Coba gunakan

Sebaiknya mulai dengan permintaan yang tidak mengubah berkas apa pun:

> Saya berencana membuat halaman web dalam bahasa Indonesia. Hal apa saja yang perlu saya perhatikan? Tolong jangan ubah berkas apa pun.

## Periksa keutuhan berkas (opsional)

Jika ingin memastikan berkas yang diunduh tidak rusak, gunakan [SHA256SUMS.txt]({{sums}}).

Letakkan SHA256SUMS.txt di folder yang sama dengan berkas ZIP yang diunduh, lalu jalankan perintah berikut di terminal. Jika `shasum` tidak tersedia, cocokkan nilai SHA-256 dengan cara lain, misalnya `Get-FileHash` di Windows PowerShell.

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

Jika baris untuk berkas yang Anda unduh menampilkan `OK`, berkas tersebut aman.

---

Alat lain: [ChatGPT / Codex]({{page_chatgpt}}) · [Gemini]({{page_gemini}})

Tampilan dan ketentuan layanan dapat berubah. Untuk informasi terbaru, silakan periksa panduan resmi setiap layanan (halaman ini terakhir diperiksa pada 14 Oktober 2026).
