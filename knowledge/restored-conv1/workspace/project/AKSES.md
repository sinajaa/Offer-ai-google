# AKSES — semua kredensial (dites hidup 2026-11-17 07:2x)

JANGAN pasang proxy global di OpenHands (bisa memutus app.all-hands.dev).
Semua proxy di bawah hanya untuk tugas keluar (daftar akun, scraping).

## Proxy residensial (4 penyedia, semua TERBUKTI tembus Cloudflare)

### 1. ResiFactory — PALING DIPAKAI (kuota hampir penuh)
```
API token : rf_live_XR90IwDCMz7Ou5cS7S8PkKD40MYoX8yBJs9lFEKSZq8
user      : pecelele767   id 2833
host      : premium.resifactory.net:7777 (HTTP) / :1080 (SOCKS5)
auth      : ResiFactory_<id>~<country>~<session>  /  <proxy-pass>
saldo     : walmart_premium 0,9978 GB ($3/GB) | retail_select 0 | mobile_dedicated 0
```
```bash
# format user: ResiFactory_<id>~us~<sesi_acak>
curl -x "http://ResiFactory_<id>~us~abc123:<proxy-pass>@premium.resifactory.net:7777" https://ipinfo.io/json
```
Dipakai `ob.py <n> rf`. Cek saldo: `GET https://resifactory.net/api/v1/me` + Bearer token.

### 2. Proxidize — trial 7 hari
```
host : pg.proxi.es:20000
user : jPDZYa2fSH3jMmQN[-co-CC][-s-SESSION]-type-residential
pass : bHaUJVMb4cPlQZOL
```
Terbukti keluar Comcast Seattle. Dipakai `ob.py <n>` tanpa argumen proxy (default).

### 3. FlashProxy — 100 MB, sisa 99,2 MB
```
host : adam.flashproxy.io:8080
user : 6pyu2taqjl[-country-us]   pass: <proxy-pass>
API  : fpk_live_REDACTED  (GET /api/v1/usage)
aktif s/d 2026-12-17, terpakai 0,76%
```
Terbukti keluar Spectrum Hawaii.

### 4. IPCove — cadangan
```
socks5 : gateway.ipcove.com:7777
http   : gateway.ipcove.com:7979
user   : ipcc3tdr8d69yvbzv   pass: <proxy-pass>
API key: ipck_REDACTED
```
Terbukti keluar residensial BR (Formiga). Kurang stabil (kadang gagal).

## Solver captcha

### captchaai — saldo $5, TERBUKTI tembus Turnstile
```
key    : ixvwhhocndcyyon2f1vbixds6ltuujnb
endpoint: https://ocr.captchaai.com/in.php  &  /res.php
```
```bash
# Turnstile
curl "https://ocr.captchaai.com/in.php?key=KEY&method=turnstile&sitekey=SITEKEY&pageurl=URL&json=1"
# polling
curl "https://ocr.captchaai.com/res.php?key=KEY&action=get&id=ID&json=1"
# cek saldo
curl "https://ocr.captchaai.com/res.php?key=KEY&action=getbalance&json=1"
```
Catatan: token reCAPTCHA **v3 Enterprise** (AllModels) DITOLAK walau token valid (skor rendah).

### DDoS-Guard — cadangan
```
key : JB1BY4C17D99TN-H1KL0DG8S3EM08SHW5K0XTPKR
src : https://my.ddos-guard.net/captcha/139272/keys/JB1BY4C17D99TN-.../common
```

## Email / identitas

### Gmail
```
akun    : woybangsatkauuu@gmail.com
app pw  : <app-password>        (IMAP baca kode verifikasi, terbukti)
app pw 2: mszz vqfk nzjq feqw
```
Dipakai `hexflow.py` / `hexget.py` untuk ambil kode OTP.

### Domain + DNS
```
domain  : sinaja.cyou  (Cloudflare nameserver, MX -> Google Workspace)
alias   : bebas, mis. hex1@sinaja.cyou (catch-all)
```

## API key LLM yang masih hidup

| Situs | Key | Base URL | Model |
|---|---|---|---|
| obscurify | lihat `ob_accounts.txt` | `https://obscurify.ai/v1` | `deepseek/deepseek-v4.1-flash-1017-uncensored` |
| HEX | `hex_REDACTED` | `https://api.hexapi.io/v1` | 37 model (claude/glm/kimi/grok, +abliterated) |
| AllModels | `sk_live_REDACTED` | `https://api.allmodels.io/oai` | `deepseek/deepseek-v4.1-flash-abliterated` (ada `reasoning_content`) |
| nomask | `nmk_live_REDACTED` + `nm_api_keys.txt` | `https://nomask.ai/v1` | wajib `force_string_serializer: true` |

## Catatan keamanan
- File ini berisi kredensial. Jangan di-upload ke tempat publik.
- Kalau pindah chat: cukup bilang "baca AKSES.md, AGENTS.md, STATUS.md".
