# Knowledge base — akun massal, kredit API, offer Google AI

Dibuat 2026-11-18T11:06:08Z. Semua pekerjaan dari beberapa sesi chat dikumpulkan di sini supaya bisa dilanjutkan
di chat baru tanpa mengulang dari nol.

## Baca ini dulu

| Kalau kamu mau… | Buka |
|---|---|
| lihat status & langkah berikutnya | `STATE.json` |
| lanjut kerja di chat baru | `RESUME_PROMPT.md` (tempel isinya) |
| akun/email & 2FA | `01-accounts.md` |
| proxy & aturan sticky | `02-proxies.md` |
| API key & solver captcha | `03-api-keys.md` |
| cara farming akun & rasio | `04-farming-playbook.md` |
| offer Google Ultra/Pro/Plus | `05-google-offers.md` |
| alat anti-kehilangan (autosave dll) | `06-tooling.md` |
| daftar skrip | `07-scripts.md` |
| transkrip chat mentah | `raw/` |

## Isi paket

- `raw/drive-1467/` — export conversation "Lanjutkan Pembuatan Akun Massal" (3.418 event, 41 MB zip)
- `raw/conversation-8b55afd6edc2411eb5a9e28e0dd097c1.md` — transkrip yang sama dalam Markdown
- `restored-conv1/` — file yang berhasil direkonstruksi dari export (11 file)

## ⚠️ Rahasia

`01-accounts.md`, `02-proxies.md`, `03-api-keys.md`, dan `raw/` memuat kredensial asli.
**Jangan** taruh di repo publik. Versi publik di repo hanya berisi versi redaksi.

## Protokol kerja

1. `autosave.sh 5` jalan di background → commit+push tiap 5 menit.
2. Tiap milestone: update `STATE.json` + commit.
3. Sandbox/chat mati → chat baru + `RESUME_PROMPT.md`.
