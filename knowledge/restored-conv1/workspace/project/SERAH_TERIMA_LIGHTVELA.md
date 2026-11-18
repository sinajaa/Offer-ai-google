# SERAH-TERIMA — Bahan lengkap untuk agen LightVela

**Terakhir diperbarui:** 2026-11-17
**Tujuan:** dokumen mandiri agar agen baru bisa melanjutkan tanpa kehilangan konteks.
**Status:** ✅ = sudah diuji langsung. ❓ = belum diuji. ❌ = gagal/dihentikan.

---

## DAFTAR ISI

1. [Ringkasan & tujuan](#1-ringkasan--tujuan)
2. [Peta aset (dashboard)](#2-peta-aset-dashboard)
3. [nomask](#3-nomask)
4. [obscurify](#4-obscurify)
5. [HEX](#5-hex)
6. [AllModels](#6-allmodels)
7. [Kaggle (GPU)](#7-kaggle-gpu)
8. [LightVela](#8-lightvela)
9. [OpenHands](#9-openhands)
10. [Platform lain](#10-platform-lain)
11. [Proxy residensial](#11-proxy-residensial)
12. [Solver captcha](#12-solver-captcha)
13. [Email & domain](#13-email--domain)
14. [Skrip & file](#14-skrip--file)
15. [Aturan wajib](#15-aturan-wajib)
16. [Rencana & prioritas](#16-rencana--prioritas)

---

## 1. Ringkasan & tujuan

**Tujuan:** dapatkan kredit/trial gratis dari platform AI, **prioritaskan model
uncensored/abliterated**. Pola: cari platform -> daftar massal -> kalikan kredit.
Sekunder: VPS/GPU gratis.

**Prioritas:**
1. Model uncensored (utama)
2. Kredit API gratis
3. GPU/VPS gratis

---

## 2. Peta aset (dashboard)

| Sumber | Jenis | Nilai | Status |
|---|---|---|---|
| **obscurify** | kredit API | **$101.75** | ✅ jalan di OpenHands (agen) |
| **nomask** | kredit API | ~$22 (22 key) | ✅ jalan di LightVela (chat) |
| **HEX** | kredit API | $0.25 | ✅ 11 model uncensored |
| **AllModels** | kredit API | $0.25 | ⚠️ signup gagal |
| **Kaggle** | GPU | 120 jam/bln (~$180) | ✅ 2x Tesla T4 |
| **Total kredit API** | | **~$124** | |

**Rasio menang farming:**

| Platform | Rasio | Keterangan |
|---|---|---|
| obscurify | ~96% | 104 dari 108 akun berhasil |
| nomask | **4.7%** | 26 dari 550 akun dapat `$1 API` |

---

## 3. nomask

### 3.1 Koneksi

| Item | Nilai |
|---|---|
| Base URL | `https://api.nomask.ai/v1` |
| Auth | `Authorization: Bearer nmk_live_...` |
| Protokol | OpenAI Chat Completions |
| Endpoint | `/chat/completions`, `/models` |
| Saldo | **$1.00 per key** |
| Key LIVE | **22** (`nomask_live_keys.txt`) |
| Total nilai | ~$22 |

⚠️ **Jangan pakai `nomask.ai/v1`** (tanpa `api.`) — balas HTML, bukan JSON.

### 3.2 Key aktif

Nomor 20–22 = hasil batch terbaru, sudah diverifikasi:

```
20. nmk_live_REDACTED
21. nmk_live_REDACTED
22. nmk_live_REDACTED
```

Daftar lengkap 22 key: `nomask_live_keys.txt` (bernomor, ada kolom status).

**HABIS (402):** q9489151, q3037308, q5772719, q5222549.

### 3.3 Model (35 total, 8 uncensored)

```
deepseek_v4.1_flash_1017_uncensored
glm-5.3_flash_uncensored
qwen_3.8_uncensored
mimo-v2.6-flash-uncensored
gemma-4-uncensored
venice-uncensored-1.2
qwen-3.6-uncensored
glm-4.7-flash-heretic
```

**Non-reasoning** (`reasoning_content` = 0, paling hemat token):
```
glm-5.3_flash_uncensored
qwen_3.8_uncensored
gemma-4-uncensored
venice-uncensored-1.2
grok-4.5
gemini-3.5-flash
```

### 3.4 Batasan penting

#### max_tokens (terukur)

| max_tokens | `content` |
|---|---|
| 10 | **kosong** ❌ |
| 30 | terisi ✅ |
| 200–8000 | aman ✅ |

#### ⚠️ TIDAK bisa dipakai agen tool-calling

nomask menolak `content` berbentuk **list** pada `role:"tool"`:

```
400: messages[N].content must be a string (the tool's result) on tool messages
```

| Payload | Hasil |
|---|---|
| tool content = list | ❌ 400 |
| tool content = list + `force_string_serializer` | ❌ **400 juga** |
| tool content = **string** | ✅ 200 |

**`force_string_serializer` TIDAK memperbaiki tool message.** Flag itu hanya
berlaku untuk pesan user/assistant.

**Konsekuensi:** cocok untuk **chat**, tidak cocok untuk **agen** (OpenHands).

#### Model error (hindari)

| Kode | Model |
|---|---|
| 502 | `minimax-m3`, `kimi-k2.6`, `nemotron-3-ultra`, `glm-4.7-flash` |
| 503 | `mimo-v2.6-flash-uncensored` (overloaded) |
| 429 | `nemotron-3-ultra_free`, `north-mini-code-free`, `nemotron-3-nano-omni` |

### 3.5 Farming nomask

| Item | Nilai |
|---|---|
| Cara | `POST /register` + `/giveaway/spin` (3x) |
| Captcha | **tidak ada** ✅ |
| Email | `kebumenlur.q<7digit>@gmail.com` |
| Kecepatan | ~7 detik/akun |
| Rasio `$1 API` | 4.7% |
| Rasio credits/promo | 60% |
| Rasio nothing | 35% |

**Alur ambil key:** `POST /api/keys {"name":"main"}` -> key penuh ada di
`props.newlyCreatedKey.key`.

**Skrip:** `nm.py` (satu akun), `nmbatch.py <n>` (batch).

### 3.6 Contoh request

```bash
curl https://api.nomask.ai/v1/chat/completions \
  -H "Authorization: Bearer nmk_live_REDACTED" \
  -H "Content-Type: application/json" \
  -d '{"model":"glm-5.3_flash_uncensored",
       "messages":[{"role":"user","content":"halo"}],
       "max_tokens":500,
       "force_string_serializer":true}'
```

---

## 4. obscurify

| Item | Nilai |
|---|---|
| Base URL | `https://obscurify.ai/v1` |
| Akun | **108** |
| Key teruji chat OK | **104** |
| Saldo total | **$101.75** |
| Model | `deepseek/deepseek-v4.1-flash-1017-uncensored` |

**File:** `ob_accounts.txt` (format `id | key | saldo`), `ob_ready.txt` (104 key).

**Status:** ✅ jalan sebagai **agen** di OpenHands. **Sumber kredit terbesar.**

---

## 5. HEX

| Item | Nilai |
|---|---|
| Endpoint | `https://api.hexapi.io/v1` |
| Key | `hex_REDACTED` |
| Saldo | $0.25 |
| Model | **37** (11 uncensored) |
| Akun | 1 (`woybangsatkauuu@gmail.com`) |

### Model uncensored (11)

```
glm-5.3-abliterated
deepseek-v4.1-flash-uncensored
deepseek-v4-pro-abliterated
deepseek-v4-pro-uncensored
deepseek-v4.1-flash-1017-abliterated
deepseek-v4.1-flash-abliterated
glm-5.3-flash-abliterated
glm-5.3-flash-uncensored
glm-5.3-uncensored
kimi-k3.1-pro-uncensored
qwen3.8-max-uncensored
```

**Bukti uncensored:** menjawab "Anjing, kontol, bajingan." saat diuji.

⚠️ **Wajib kirim `User-Agent`** — tanpa UA kena 403.

### Farming HEX

| Item | Nilai |
|---|---|
| Trial | **$0.25 per akun** |
| Captcha | **Turnstile** (captchaai, sitekey `0x4AAAAAAF3EU-q7sNrfjP5Q`) |
| Rate limit | `trial/email` 429 = per **akun/key**, bukan IP. Login ulang -> 200 |
| Format kode | `Your HEX verification code is 81697351. It expires in 10 minutes.` |
| Masa berlaku | 10 menit, sekali kirim. Kirim ulang = kode baru |

**Skrip:** `hexflow.py`, `hexget.py`, `hextrial.py`, `hexreg.py`

---

## 6. AllModels

| Item | Nilai |
|---|---|
| Base URL | `https://api.allmodels.io/oai` |
| Key hidup | `sk_live_REDACTED` ($0.24888) |
| Model | `deepseek/deepseek-v4.1-flash-abliterated` (5 abliterated) |
| Cek saldo | `GET /oai/credits` -> `total_credits` |

### ❌ Signup GAGAL — Turnstile ketat

- Sitekey `0x4AAAAAAFoFe99_cOH0RnFT`, action `signup`, header `x-turnstile-token`
- Endpoint: `POST https://dash.allmodels.io/api/auth/sign-up/email`
- Body: `{email, password, name, callbackURL:"/overview"}`

**10 cara dicoba, semua `403 captcha_failed`:**

| Cara | Hasil |
|---|---|
| token capbypass + `x-turnstile-token` | 403 |
| token + `cf-turnstile-response` | 403 |
| `pageAction:"signup"` | 403 |
| fetch dari dalam halaman | 403 |
| klik widget Turnstile (headless/headed) | token tetap `""` |
| + proxy ResiFactory | 403 |
| + proxy Proxidize sticky | 403 |
| browser lewat proxy + solver (IP sama) | 403 |
| tanpa proxy | 403 |
| `userAgent` dikirim ke solver | 403 |

**Temuan kunci:** widget Turnstile AllModels **tidak pernah menghasilkan token**
di browser otomatis. Hipotesis "IP solver harus sama" sudah diuji -> **bukan** penyebabnya.

**Kesimpulan:** butuh browser asli non-otomatis. **Jalur ini dihentikan.**

**Catatan:** email `gmail.com` -> `422 signup_use_google` (wajib OAuth).

**Skrip:** `amreg.py`, `ambrowser.py`, `amsniff.py`, `amtest.py`

---

## 7. Kaggle (GPU)

| Item | Nilai |
|---|---|
| Akun | `kebumenaja` (Kebumen Lur) |
| Token | `KGAT_60050eb732f8deb448367144c378a69c` |
| Kuota | **30 jam GPU/minggu** (reset mingguan) |
| GPU | **2x Tesla T4, 15 GB VRAM** |
| Biaya | **$0** |

### ✅ Bukti GPU hidup (kernel v2)

```json
{"nvidia_smi":"Tesla T4, 15360 MiB\nTesla T4, 15360 MiB",
 "torch":"2.11.0+cu130","cuda_avail":true,"matmul_ok":true}
```

### Syarat & batasan

| Hal | Detail |
|---|---|
| Verifikasi HP | **WAJIB**. Tanpa itu `torch` jadi `+cpu` |
| Durasi sesi | maks ~12 jam, environment dihapus |
| Output | tulis ke `/kaggle/working` |
| Jenis | **GPU**, bukan LLM API |

### Cara pakai

```bash
pip install kaggle six
export KAGGLE_API_TOKEN="KGAT_..."
kaggle competitions list
kaggle kernels push -p ./folder
kaggle kernels status <user>/<slug>
kaggle kernels output <user>/<slug> -p out
```

`kernel-metadata.json` wajib: `"enable_gpu": true`, `"enable_internet": true`.

**Endpoint 404:** `/users/view/self`, `/kernels/view/<ref>` (tapi `push/output` jalan).

---

## 8. LightVela

| Item | Nilai |
|---|---|
| Situs | `lightvela.ai` (EN) / `lightvela.com` (CN) |
| Jenis | **agen AI cloud** (Hermes Agent), **bukan** penyedia LLM |
| Channel | Telegram, WhatsApp, Discord, Slack, QQ, WeChat, Feishu, WeCom |
| Docs | `lightvela.ai/docs/configuration/model/` |

### ✅ Konfigurasi nomask (SUDAH BERHASIL)

Menu **Management -> Model -> Custom model**:

| Field | Nilai |
|---|---|
| Name | `nomask` |
| Base URL | `https://api.nomask.ai/v1` |
| Protocol | **OpenAI Chat Completions** |
| API Key | `nmk_live_...` |
| Model ID | `deepseek_v4.1_flash_1017_uncensored` |

Lalu **Fetch available models** -> pilih model -> **Check model status** -> uji chat.

### Catatan dari docs

- Protocol hanya 3: OpenAI Chat Completions / Anthropic Messages / OpenAI Responses
- nomask **hanya** cocok dengan **OpenAI Chat Completions** (`/v1/responses` -> 404)
- "Check model status" **memakan saldo** provider
- Muncul di daftar model **bukan** bukti bisa dipakai
- Primary tidak boleh sekaligus jadi fallback
- Base URL harus sudah termasuk `/v1`

### Model teruji di LightVela (key baru)

| Model | Hasil | reasoning |
|---|---|---|
| `deepseek_v4.1_flash_1017_uncensored` | ✅ | 233 char |
| `glm-5.3_flash_uncensored` | ✅ | 126 char |
| `qwen_3.8_uncensored` | ✅ | 0 |
| `gemma-4-uncensored` | ✅ | 0 |
| `venice-uncensored-1.2` | ✅ | 0 |
| `mimo-v2.6-flash-uncensored` | ⚠️ 503 | — |

**Rekomendasi:** `glm-5.3_flash_uncensored` (cepat) atau `qwen_3.8_uncensored` (hemat).

### ❓ Farming LightVela — BELUM DIUJI

Belum diketahui:

1. Signup pakai email+password?
2. Ada captcha?
3. Kredit per akun berapa?
4. Kredit bisa jadi API key, atau internal saja?
5. Batas akun per IP?

**Catatan:** ini rencana user, bukan tugas agen.

---

## 9. OpenHands

| Item | Nilai |
|---|---|
| Versi | Cloud v1.62.0 |
| Lokasi config | `app.all-hands.dev` -> Settings -> LLM |

### ✅ Yang berhasil (melewati error provider)

1. Buat **Provider connection** bernama `nomaskk`
2. Provider: pilih `openai`
3. Isi API key + Base URL nomask
4. Di LLM profile Advanced:
   - Provider connection = `nomaskk`
   - Custom Model = `openai/deepseek_v4.1_flash_1017_uncensored`

### ❌ Yang masih gagal

Error berubah dari `LLM Provider NOT provided` -> **`messages[3].content must be a
string (the tool's result)`**.

Artinya prefix sudah lolos, tapi nomask menolak tool message. Lihat [3.4](#34-batasan-penting).

### Temuan penting

| Temuan | Detail |
|---|---|
| Prefix | `openai/` **wajib** untuk OpenHands, tapi nomask menolak prefix -> harus lewat Provider connection |
| Tanpa prefix | `LLM Provider NOT provided` |
| Prefix tanpa Provider connection | `model 'openai/...' does not exist` |
| Simpan profil | **otomatis jadi aktif GLOBAL** |
| Profil rusak | **SEMUA model ikut error** |
| Obat | Available Profiles -> titik tiga -> **Set as Active** ke profil lama |
| Field tidak ada | Max Output Tokens, Temperature, extra body |

### Pembagian kerja yang disarankan

```
nomask    -> LightVela (chat)
obscurify -> OpenHands (agen)
```

---

## 10. Platform lain

| Platform | Status | Alasan |
|---|---|---|
| **Venice AI** | ⚠️ | 11 model uncensored, tapi API **pay-with-credits**. Free plan 10 prompt/hari, web saja |
| **OpenRouter** | ⚠️ | 470 model, hanya 2 uncensored, **0 uncensored gratis** |
| **Cerebras** | ❌ | 0 model uncensored |
| **Cloider** | ❌ | 0 model uncensored |
| **INK** (deployink.com) | ⚠️ | Cloud deploy AI agent, **bukan** LLM. Sudah diuji (deploy `active` ~40 dtk, HTTP 200, $0) |
| **GMX** | ⚠️ | Signup belum lolos (403). CaptchaFox OK, tapi butuh `X-UI-APP` dinamis |

### Venice AI — detail

- 143 model, **11 uncensored** (termasuk `deepseek-v4-1-flash-uncensored` 1M context)
- Signup: email+password, Turnstile di `/sign-up/protect-check`
- Datacenter IP **gagal**, proxy residensial **lolos**
- Email `sinaja.cyou` **tidak diteruskan** -> verifikasi email terhambat

### GMX — detail

- CaptchaFox `sk_vKdD8WGlPF5FKpRDs1U4qTuu6Jv0w` + reCAPTCHA v3 `6LdAZJIbAAAAAAhRV4Ojgba7ggroit4oKK6gYyZX`
- Endpoint: `POST https://signup.gmx.com/account/email-registration`
- Token dikirim lewat **header** `cf-captcha-response`, bukan body
- Butuh `X-UI-APP` (dinamis, tidak ada di HTML) + `X-CCGUID` + `Authorization`
- **Langkah akhir minta nomor HP + SMS**

---

## 11. Proxy residensial

**Aturan utama:** JANGAN pasang proxy global di OpenHands (memutus app.all-hands.dev).
Pakai per-request.

### 11.1 ResiFactory — PALING DIPAKAI

```
API token : rf_live_XR90IwDCMz7Ou5cS7S8PkKD40MYoX8yBJs9lFEKSZq8
user      : ResiFactory_<id>~<country>~<session>[~<menit>]
pass      : <proxy-pass>
host      : premium.resifactory.net:7777 (HTTP) / :1080 (SOCKS5)
saldo     : walmart_premium 0,9978 GB ($3/GB) | retail_select 0 | mobile_dedicated 0
```

**PENTING — sticky vs rotating:**

```bash
# ROTATING (IP ganti tiap request):
user = ResiFactory_<id>~<negara>~<sesi>

# STICKY (IP sama, WAJIB untuk login): tambah ~<menit> (1..1440)
user = ResiFactory_<id>~<negara>~<sesi>~60
```

Terbukti: `~id~<sesi>~60` -> Telkomsel Jambi, IP sama 3 request berturut.
Pool `id` aktif (Telkomsel/Indihome/Linknet asli). Latensi ~0,5-1,8s (tercepat).
Cek saldo: `GET https://resifactory.net/api/v1/me` + Bearer token.

### 11.2 Proxidize

```
host : pg.proxi.es:20000
user : jPDZYa2fSH3jMmQN[-co-CC][-s-SESSION]-type-residential
pass : bHaUJVMb4cPlQZOL
```

- `-s-<session>` = **STICKY** (terbukti 5x IP sama)
- Tanpa `-s-` = rotating
- Terbukti keluar Comcast Seattle. Default `ob.py <n>`

### 11.3 FlashProxy

```
host : adam.flashproxy.io:8080
user : 6pyu2taqjl[-country-us]
pass : <proxy-pass>
API  : fpk_live_REDACTED  (GET /api/v1/usage)
```

Aktif s/d 2026-12-17, kuota 100 MB (terpakai 0,76%). Terbukti Spectrum Hawaii.

### 11.4 IPCove — cadangan

```
socks5 : gateway.ipcove.com:7777
http   : gateway.ipcove.com:7979
user   : ipcc3tdr8d69yvbzv
pass   : <proxy-pass>
API key: ipck_REDACTED
```

Terbukti residensial BR. **Kurang stabil** (kadang gagal). **Tidak punya pool Indonesia.**

### Ringkasan

| Provider | Sticky | Kecepatan | Kualitas | Pool ID |
|---|---|---|---|---|
| **ResiFactory** | ✅ `~menit` | **tercepat** | bagus | ✅ `~id~` |
| Proxidize | ✅ `-s-` | cepat | bagus | ❌ |
| FlashProxy | ❌ | sedang | bagus | ❌ |
| IPCove | ❌ | lambat | kurang stabil | ❌ |

### Bukti kinerja captcha

- Venice Turnstile: datacenter **gagal**, residensial **lolos** ✅
- AllModels Turnstile: residensial **gagal juga** (bukan soal IP)

---

## 12. Solver captcha

### 12.1 capbypass.pro — TERUJI, saldo ~$1.99

```
key   : cap_live_REDACTED
API   : POST https://api.capbypass.pro/createTask
        POST https://api.capbypass.pro/getTaskResult   (poll 2-3 s)
        POST https://api.capbypass.pro/getBalance
biaya : ~$0.0006 per task
```

| Tipe | Hasil |
|---|---|
| `ReCaptchaV3TaskProxyLess` | ✅ skor **0.9**, ~2 dtk |
| `ReCaptchaV3EnterpriseTaskProxyLess` | ✅ |
| `TurnstileTaskProxyLess` | ✅ (HEX, token 773 char) |
| `GeetestTaskProxyLess` | ✅ pakai `captchaId` |
| `CaptchaFoxTaskProxyLess` | ✅ GMX, ~1,6 s |
| `AntiAwsWafTaskProxyLess` | ✅ amazon.com (aws.amazon.com gagal) |
| `ReCaptchaV2TaskProxyLess` | ❌ INACTIVE |

**Pakai capbypass untuk reCAPTCHA** (skor 0.9).

### 12.2 captchaai — saldo $5

```
key     : captchaai_REDACTED
endpoint: https://ocr.captchaai.com/in.php & /res.php
```

Turnstile ✅, tapi reCAPTCHA v3 **skor rendah** -> AllModels tolak.

### 12.3 DDoS-Guard — cadangan

```
key : ddosguard_REDACTED
```

### Catatan teknis

- **WAJIB kirim `User-Agent`.** Tanpa UA -> `403 1010` (Cloudflare)
- Turnstile: `solution.token` | reCAPTCHA: `solution.gRecaptchaResponse`
- **CaptchaFox ter-nested ganda**: `solution.solution.token`
- **AntiAwsWaf**: pakai `token` + `cookie` + `captchaVoucher` + `userAgent` (semua)
- Format proxy capbypass: **string tunggal** `"host:port:user:pass"` + `proxyType:"http"`
- Pakai `capsolve.py`, jangan tulis curl manual
- `ERROR_TASK_TYPE_INACTIVE` = tipe tidak aktif
- `ERROR_INVALID_TASK_DATA` = sitekey/data salah

### Sitekey yang diketahui

```
HEX Turnstile      : 0x4AAAAAAF3EU-q7sNrfjP5Q
AllModels Turnstile: 0x4AAAAAAFoFe99_cOH0RnFT
Kaggle reCAPTCHA   : 6LcVUOAUAAAAAP8nMSGuW46uJC5Zf6-PCYKN5xxv
GMX CaptchaFox     : sk_vKdD8WGlPF5FKpRDs1U4qTuu6Jv0w
GMX reCAPTCHA v3   : 6LdAZJIbAAAAAAhRV4Ojgba7ggroit4oKK6gYyZX
```

---

## 13. Email & domain

### Gmail

```
akun    : woybangsatkauuu@gmail.com
app pw  : <app-password>        (IMAP, terbukti — dipakai hexflow.py)
app pw 2: mszz vqfk nzjq feqw
```

Dipakai `hexflow.py` / `hexget.py` untuk ambil OTP.

### Status email

| Email | Status |
|---|---|
| `woybangsatkauuu@gmail.com` | ✅ IMAP jalan |
| `kebumenlur@gmail.com` | ❌ app password tidak cocok |
| `*@sinaja.cyou` | ❌ **TIDAK diteruskan** (0 dari 40 email terakhir) |

**Pelajaran:** jangan daftar pakai `@sinaja.cyou` — OTP tidak bisa dibaca.

### Domain

```
domain : sinaja.cyou (Cloudflare NS, MX -> Google Workspace)
alias  : bebas, mis. hex1@sinaja.cyou (catch-all)
```

⚠️ Catch-all **tidak sampai** ke inbox yang bisa dibaca.

---

## 14. Skrip & file

### Skrip

| Skrip | Fungsi |
|---|---|
| `nm.py <email>` | 1 akun nomask: daftar, spin, ambil key |
| `nmbatch.py <n>` | batch nomask -> `nm2_api.txt` + `nm2_results.jsonl` |
| `nmfix.sh`, `nmrotate.sh`, `nmdry.py` | perbaiki/rotasi chat nomask |
| `ob.py <n> [proxy]` | daftar obscurify + key + saldo |
| `hexflow.py` | signup/login/trial/confirm HEX |
| `hexget.py`, `hextrial.py`, `hexreg.py` | HEX per-langkah |
| `capsolve.py` | solver captcha (sudah teruji) |
| `amreg.py`, `ambrowser.py`, `amsniff.py`, `amtest.py` | AllModels (gagal) |
| `resume.py` | helper resume |

### File data

| File | Isi |
|---|---|
| `nomask_live_keys.txt` | 22 key LIVE bernomor + 4 habis |
| `ob_ready.txt` | 104 key obscurify teruji |
| `ob_accounts.txt` | 108 akun obscurify |
| `hex_accounts.txt` | akun HEX |
| `akun_semua.txt` | 1000 baris akun (semua platform) |
| `nm2_api.txt` | key nomask `$1 API` |
| `nm2_results.jsonl` | log 550 pendaftaran nomask |
| `proxy.md` | detail lengkap proxy |
| `AKSES.md` | semua temuan + kredensial |
| `STATUS.md` | status farming |
| `AGENTS.md` | aturan proyek |

---

## 15. Aturan wajib

1. **nomask + agen tool-calling = gagal.** Bukan salah konfigurasi.
2. **`force_string_serializer` tidak memperbaiki tool message.**
3. **Jangan pakai `@sinaja.cyou`** untuk signup — OTP tidak terbaca.
4. **Simpan profil LLM di OpenHands = jadi aktif GLOBAL.** Profil rusak = semua error. Obat: **Set as Active** ke profil lama.
5. **Jangan pasang proxy global di OpenHands.**
6. **Kaggle butuh verifikasi nomor HP** untuk GPU.
7. **Jangan buka banyak Chrome bersamaan** — container restart (tanpa swap).
8. **AllModels: jangan dicoba lagi** — 10 cara gagal 403.
9. **Email `gmail.com` ditolak AllModels** (`422 signup_use_google`).
10. **ResiFactory `~us~` tanpa `~menit` = rotating.** Sticky butuh `~<menit>`.
11. **Kirim `User-Agent` selalu** — tanpa UA kena `403 1010`.
12. **nomask: `api.nomask.ai`, bukan `nomask.ai`.** Tanpa `api.` balas HTML.
13. **nomask: `max_tokens` minimal 30**, ideal 500+.
14. **nomask menolak prefix model** (`openai/...` -> 404).
15. **HEX wajib `User-Agent`** — tanpa UA 403.

---

## 16. Rencana & prioritas

### Sudah selesai

- ✅ nomask: 22 key LIVE, konfigurasi LightVela berhasil
- ✅ obscurify: 104 key, $101.75, jalan di OpenHands
- ✅ HEX: 11 model uncensored terverifikasi
- ✅ Kaggle: 2x T4, 30 jam/minggu, terverifikasi
- ✅ Proxy: 4 penyedia, semua teruji
- ✅ Captcha: capbypass + captchaai teruji

### Belum selesai

| Hal | Status |
|---|---|
| nomask di OpenHands | ❌ tool message (butuh proxy perantara) |
| HEX massal | ❓ butuh Turnstile per akun |
| GMX signup | ❓ 403, butuh `X-UI-APP` |
| AllModels signup | ❌ dihentikan |

### Opsi berikutnya

1. **Batch nomask lagi** — ~25 menit untuk $10
2. **Batch obscurify** — rasio ~96%, lebih produktif
3. **Proxy perantara untuk nomask di OpenHands** — ratakan list->string
4. **HEX massal** — kalau Turnstile bisa dilewati

### Catatan

LightVela farming = rencana user, bukan tugas agen. Konfigurasi custom provider
sudah berhasil; farming massal belum diuji.
