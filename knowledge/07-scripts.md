# 07 — Inventaris skrip

## Hasil rekonstruksi dari export conversation (drive-1467)

| File | Fungsi |
|---|---|
| `workspace/project/AKSES.md` | daftar akses/kredensial ringkas |
| `workspace/project/SERAH_TERIMA_LIGHTVELA.md` | dokumen serah-terima aset |
| `workspace/project/STATUS.md` | status pekerjaan saat itu |
| `workspace/project/ambrowser.py` | automasi browser untuk pendaftaran |
| `workspace/project/amreg.py` | registrasi akun massal |
| `workspace/project/amsniff.py` | sniff endpoint/flow registrasi |
| `workspace/project/amtest.py` | uji hasil registrasi |
| `workspace/project/capsolve.py` | wrapper solver captcha |
| `workspace/project/check_keys.py` | cek validitas/saldo key |
| `workspace/project/gmxtest.py` | uji layanan GMX/mail |
| `workspace/project/mf/build-prompt.md` | prompt build game make.fun |

File lengkap ada di `knowledge/restored-conv1/`.

## Skrip dari dokumen serah-terima

| Skrip | Fungsi |
|---|---|
| `nm.py <email>` | 1 akun nomask: daftar, spin, ambil key |
| `nmbatch.py <n>` | batch nomask |
| `ob.py <n>` | batch obscurify (default proxy Proxidize) |
| `hexflow.py` / `hexget.py` | daftar HEX + ambil OTP lewat IMAP |

## Skrip dari sesi offer Google

| Skrip | Fungsi |
|---|---|
| `build_link.py` | bangun link `ear` dari token repo (Ultra 20 TB / 30 TB) |
| `claim_test.py` | buka link dengan akun login, klasifikasi hasil |
| `signup*.py` | eksperimen signup Google US (email temp, QR, dsb) |
| `paybind*.py` | eksperimen tempel kartu di Play/Wallet |
| `monitor.py` | versi lokal pemantau offer |
| `autosave.sh` | commit+push+zip berkala |
| `rebuild_from_conversation.py` | rekonstruksi file dari export chat |

## Aturan penamaan

`<fungsi>_<target>.py`, contoh `signup_ext.py` = signup pakai email eksternal.
Jangan bikin versi `_fix`, `_final`, `_v2` — timpa file yang sama.
