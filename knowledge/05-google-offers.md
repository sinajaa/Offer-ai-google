# 05 — Offer Google AI (Ultra / Pro / Plus)

## Ringkasan status per 2026-11-18

| Jalur | Status | Catatan |
|---|---|---|
| Ultra 20 TB 12 bulan via link `ear` | ❌ **ditutup (patched)** | semua link menghasilkan "Terjadi error" |
| Ultra 30 TB (`g1.play.ai.pro`) | ❌ ditutup | issue #19: "1 bulan juga mati" |
| AI Pro student 12 bulan (kampus US) | ✅ hidup | SheerID + metode bayar |
| AI Plus student 12 bulan (kampus ID) | ✅ hidup | 400 GB, Rp 0/bln |
| AI Plus promo Rp 7.500 bulan pertama | ✅ hidup | tanpa verifikasi mahasiswa |

## Cara kerja jalur token (untuk referensi)

Link `tokenized.play.google.com/eacquire/multiline` membawa payload `ear` berisi:
- `PATH = /plans?g1_last_touchpoint=37&g1_landing_page=1&otzr=1`
- item: `subs:com.google.android.apps.subscriptions.red:g1.play.20tb` + token offer (`eft-12month`)
- fingerprint browser di `ear[4]`

Repo `gylive/google-ultra` menyediakan `buildUrl()` + token. Parameter `jsh` bawaannya sudah 404;
loader gapi valid bisa diambil dari `https://apis.google.com/js/api.js`.

## Bukti offer sudah ditutup (2026-11-18)

- Issue #19 "12个月的失效了，1个月还能开" lalu "1个月的突然又打不开了"
- Issue #20 "已经确认拉闸了"
- Issue #26 script frida resmi: "❌ 没有免费试用"
- Issue #18 "item you requested is not available for purchase"
- Issue #15 "漏洞被堵"
- 5 repo klon memakai token identik (sha1 `88e273bb69`, `12d4d4c791`) → tidak ada token baru
- Uji sendiri: akun co.id → error; akun Gmail baru via VPN US (dibuat user) → error sama

## Temuan penting soal akun Indonesia (co.id)

- `SetSID` diarahkan ke `accounts.google.co.id`
- Google One menampilkan harga Rp (Lite 2.400 / Basic 5.000 / AI Plus 7.500)
- Metode bayar: DANA terpasang + opsi DOKU/GoPay/ShopeePay
- Offer Ultra adalah offer Play **US** → akun ID tidak akan pernah melihat $0

## Jalur resmi yang hidup

Halaman: `https://gemini.google/id/students/` · klaim: `https://one.google.com/ai-student?plans=1%2C2`
Syarat (dari `one.google.com/offer/studentoffer8`, diperbarui 19 Agu 2026):

- 18+, mahasiswa aktif di institusi pada negara tempat paket didukung
- verifikasi lewat **SheerID**
- akun Google pribadi, bukan akun terawasi / family group
- **wajib punya metode pembayaran** saat mendaftar
- klaim sebelum **31 Desember 2026**
- setelah 12 bulan auto-renew ke harga normal

**Tier mengikuti negara kampus**: kampus US → AI Pro (5 TB) · kampus ID → AI Plus (400 GB).

## Percobaan membuat akun US (hasil)

Berhasil sampai: nama → DOB → email → kode email → password.
Blocker:
1. `crossflowverification` (scan QR device): "device used too many times" (HP user kena limit)
2. `signup/error/1`: "Sorry, we could not create your Google Account" (anti-abuse)

Teknis yang dipakai: proxy residensial US (ResiFactory sticky), Chromium **headed** di Xvfb,
`--disable-http2`, email temp `mail.tm` untuk baca kode verifikasi otomatis.

## Kartu "1 dollar" dari tweet

BIN `531790` = **Mastercard prepaid Turki** (BPN Ödeme). Bukan US. Kalau diterima, region Play jadi
TR, bukan US → offer US tetap tidak muncul.

## Pemantauan

Repo: `sinajaa/Offer-ai-googl` (monitor Actions tiap 20 menit + dashboard Pages).
Sinyal: hash token berubah, repo baru dengan SKU sama, issue berbunyi "buka lagi".
