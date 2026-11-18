# 03 — API key & layanan

> Kredensial. Simpan di repo privat.

## Ringkasan nilai aset

| Sumber | Jenis | Nilai | Status |
|---|---|---|---|
| obscurify | kredit API | $101.75 (104 key) | ✅ jalan sebagai agen |
| nomask | kredit API | ~$22 (22 key × $1) | ✅ chat saja |
| HEX | kredit API | $0.25 | ✅ 37 model |
| capbypass | solver captcha | saldo ~$1.99 | ✅ reCAPTCHA/Turnstile |
| captchaai | solver captcha | $5 | ⚠️ reCAPTCHA skor rendah |

## nomask

- Base URL `https://api.nomask.ai/v1`, header `Authorization: Bearer nmk_live_...`
- Saldo **$1 per key**. Farming: `POST /register` + `/giveaway/spin` (3x), tanpa captcha.
- Rasio: 4.7% dapat $1 API, 60% credits, 35% kosong. ~7 detik/akun.
- ⚠️ Tidak bisa untuk agen tool-calling (`role:tool` harus string).
- Model error: 502 minimax-m3/kimi-k2.6/nemotron-3-ultra/glm-4.7-flash; 503 mimo-v2.6-flash; 429 nemotron-3-ultra_free.
- Key yang ditemukan di riwayat:

  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`
  - `nmk_live_REDACTED`

## obscurify
- Base URL `https://obscurify.ai/v1`, model `deepseek/deepseek-v4.1-flash-1017-uncensored`
- 108 akun, 104 key teruji. File `ob_accounts.txt` (id | key | saldo), `ob_ready.txt`.

## HEX
- Endpoint `https://api.hexapi.io/v1`; **wajib User-Agent** (tanpa UA = 403).
- 37 model, 11 uncensored (glm-5.3-abliterated, deepseek-v4.1-flash-uncensored, dll).
- Trial $0.25/akun. Key:

  - `hex_REDACTED`
  - `hex_REDACTED`
  - `hex_REDACTED`
  - `hex_REDACTED`
  - `hex_REDACTED`

## Solver captcha — 3 akun, 3 penyedia

Diverifikasi live 2026-11-18 lewat endpoint balance masing-masing.

| # | Penyedia | Akun | Key | Saldo live | Biaya | Status |
|---|---|---|---|---|---|---|
| 1 | **capbypass.pro** | 1 | `cap_live_REDACTED` | **$1.9563** | ~$0.0006/task | ✅ utama |
| 2 | **captchaai** (ocr.captchaai.com) | 1 | `captchaai_REDACTED` | **$5** | per task | ⚠️ cadangan |
| 3 | **DDoS-Guard solver** | 1 | `ddosguard_REDACTED` | tidak ada API saldo | — | ⚠️ cadangan |

Catatan: total 3 akun, bukan kumpulan akun per penyedia — satu key per penyedia.

### 1. capbypass.pro (yang dipakai)

- API: `POST https://api.capbypass.pro/createTask`, `/getTaskResult` (poll 2–3 dtk), `/getBalance`
- Hasil uji:

| Tipe | Hasil |
|---|---|
| `ReCaptchaV3TaskProxyLess` | ✅ skor 0.9, ~2 dtk |
| `ReCaptchaV3EnterpriseTaskProxyLess` | ✅ |
| `TurnstileTaskProxyLess` | ✅ (token 773 char, HEX) |
| `GeetestTaskProxyLess` | ✅ pakai `captchaId` |
| `CaptchaFoxTaskProxyLess` | ✅ GMX, ~1,6 dtk |
| `AntiAwsWafTaskProxyLess` | ✅ amazon.com (aws.amazon.com gagal) |
| `ReCaptchaV2TaskProxyLess` | ❌ INACTIVE |

### 2. captchaai (cadangan)

- Endpoint: `https://ocr.captchaai.com/in.php` & `/res.php`; cek saldo `?key=...&action=getbalance`
- Turnstile ✅ (dipakai HEX, sitekey `0x4AAAAAAF3EU-q7sNrfjP5Q`), reCAPTCHA v3 skor rendah → AllModels menolak.

### 3. DDoS-Guard solver (cadangan terakhir)

- Hanya key, tanpa dashboard saldo yang terdokumentasi. Dipakai kalau dua di atas gagal.

### Yang pernah gagal walau pakai solver

| Skenario | Hasil |
|---|---|
| AllModels: token capbypass + `x-turnstile-token` | 403 |
| AllModels: token + `cf-turnstile-response` | 403 |
| klik widget Turnstile manual (headless & headed) | token tetap kosong |
| + proxy Resifactory / Proxidize sticky | 403 |

Artinya: AllModels bukan soal token, tapi fingerprint/flow-nya.

## Proxy API key
- FlashProxy: `fpk_live_...` (GET /api/v1/usage)
- IPCove: `ipck_...`

  - `fpk_live_REDACTED`
  - `ipck_REDACTED`

## Catatan keamanan
- Semua key di atas pernah tampil di chat; anggap sudah setengah publik. Rotasi kalau dipakai produksi.
- Jangan commit file ini ke repo publik.

## Verifikasi live — 2026-11-18

| Layanan | Tercatat | Aktif sekarang | Bukti |
|---|---|---|---|
| obscurify | 108 akun / 104 key | **tidak diketahui** — key-nya tidak tersimpan | hanya ada di `ob_accounts.txt`/`ob_ready.txt` (sandbox lama, hilang); tidak ada di export chat |
| nomask | 33 key unik | **0** | semua balas `401 invalid_api_key` (uji `/v1/models` dan `/v1/chat/completions`) |
| HEX | 3 key | **≥2 aktif** | `hex_T8z8…` dan `hex_JXId…` → `/v1/models` 200 |
| capbypass | 1 | ✅ saldo $1.9563 | `POST /getBalance` |
| captchaai | 1 | ✅ saldo $5 | `?action=getbalance` |

### Kesimpulan

- **nomask: aset $22 sekarang Rp 0.** Key lama dicabut/di-rotasi. Kalau mau lagi, farming ulang
  (rasio 4.7%, ~7 detik/akun, tanpa captcha).
- **obscurify: inventaris ingat, key tidak.** Butuh file `ob_accounts.txt` (id | key | saldo) atau
  login ke akun obscurify untuk daftar ulang key.
- **HEX masih hidup** untuk model listing; saldo $0.25 (endpoint balance tidak tersedia publik).
- **Solver captcha masih hidup** dan itu aset paling siap pakai sekarang.

Detail hasil probe nomask: `nmask_status.json`.
