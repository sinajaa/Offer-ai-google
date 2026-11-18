# 04 — Playbook farming akun & kredit API

## Prinsip dasar

1. **Isolasi per akun**: satu akun = satu proxy sticky + satu email + satu fingerprint. Jangan campur.
2. **Proxy menentukan lolos/tidak**, bukan teknik form. Turnstile Venice: datacenter ❌, residensial ✅.
3. **Volume kecil tapi konsisten** lebih aman daripada burst; platform mulai memblokir pola.
4. **Catat rasio**, bukan perasaan: tiap batch harus punya angka success rate.

## nomask (rasio rendah, tapi instan)

| Item | Nilai |
|---|---|
| Endpoint | `POST https://api.nomask.ai/v1/register`, `/giveaway/spin` (3x) |
| Captcha | tidak ada |
| Email | `kebumenlur.q<7digit>@gmail.com` (fiktif) |
| Kecepatan | ~7 detik/akun |
| Hasil | 4.7% dapat key $1 · 60% credits · 35% kosong |

Langkah: daftar → spin 3x → kalau dapat, `POST /api/keys {"name":"main"}`, key penuh ada di
`props.newlyCreatedKey.key`.

Batasan penting (sudah diuji):
- `max_tokens` 10 → `content` kosong. Pakai ≥30, aman 200–8000.
- Tidak bisa dipakai agen: `role:"tool"` harus string; `force_string_serializer` tidak menolong.

## obscurify (aset terbesar)

- 108 akun, 104 key teruji chat, total $101.75.
- Model: `deepseek/deepseek-v4.1-flash-1017-uncensored`.
- File: `ob_accounts.txt` (id | key | saldo), `ob_ready.txt`.
- Rasio ~96% (104/108) — jauh lebih baik daripada nomask.

## HEX

- Trial $0.25/akun, 37 model (11 uncensored). **Wajib User-Agent**, tanpa UA 403.
- OTP dibaca dari Gmail via IMAP (`hexflow.py`, `hexget.py`) memakai app password.
- Akun uji: `woybangsatkauuu@gmail.com`.

## Yang pernah gagal (jangan diulang tanpa alasan baru)

| Platform | Kegagalan | Sebab |
|---|---|---|
| AllModels | signup gagal | Turnstile menolak walau residensial |
| sinaja.cyou (catch-all) | OTP tidak masuk | MX ke Workspace, catch-all mati (0/40) |
| Proxidize di sandbox | `ERR_TUNNEL_CONNECTION_FAILED` | kredensial/koneksi |
| FlashProxy untuk Google | timeout | proxy tidak cocok untuk domain Google |

## Etika & risiko

Semua di atas adalah pendaftaran massal ke layanan pihak ketiga. Risiko: akun diblokir, key dicabut,
IP residensial di-flag. Jangan pakai akun utama, jangan taruh data pribadi.
