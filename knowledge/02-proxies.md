# 02 — Proxy residensial

> Aturan utama: JANGAN pasang proxy global di sandbox (memutus app.all-hands.dev). Pakai per-request.

## ResiFactory (paling dipakai, pool Indonesia + US)

```
host  : premium.resifactory.net:7777 (HTTP) / :1080 (SOCKS5)
user  : ResiFactory_<id>~<negara>~<sesi>[~<menit>]   # ~menit = sticky
pass  : <proxy-pass>
```
- Rotating: tanpa `~menit`. Sticky: tambah `~60` (1..1440).
- Terbukti: `~us~<sesi>~120` keluar Spectrum California/Florida; `~id~<sesi>~60` Telkomsel Jambi.
- Catatan penting: Chromium harus `--disable-http2` kalau lewat proxy ini, kalau tidak Google hang.

## Proxidize

```
host : pg.proxi.es:20000
user : jPDZYa2fSH3jMmQN[-co-US][-s-SESSION]-type-residential
pass : <lihat secret / dokumen serah-terima>
```
- `-s-<sesi>` = sticky. Terbukti keluar Comcast Seattle.
- Di sandbox ini sempat gagal `ERR_TUNNEL_CONNECTION_FAILED` (kredensial/koneksi).

## FlashProxy

```
host : adam.flashproxy.io:8080
user : 6pyu2taqjl-country-us
pass : <proxy-pass>
api  : fpk_live_… (cek /api/v1/usage)
```
- Kuota 100 MB, aktif s/d 2026-12-17. Google lewat proxy ini timeout.

## IPCove (cadangan)

```
socks5 : gateway.ipcove.com:7777
http   : gateway.ipcove.com:7979
user   : ipcc3tdr8d69yvbzv
pass   : <proxy-pass>
```
- Kurang stabil, tanpa pool Indonesia.

### Host:port yang muncul di riwayat

- `premium.resifactory.net:7777` (muncul 98x)
- `pg.proxi.es:20000` (muncul 78x)
- `adam.flashproxy.io:8080` (muncul 26x)
- `gateway.ipcove.com:7777` (muncul 20x)
- `gateway.ipcove.com:7979` (muncul 17x)
- `npremium.resifactory.net:7777` (muncul 7x)
- `nadam.flashproxy.io:8080` (muncul 7x)
- `npremium.resifactory.net:1080` (muncul 4x)
- `namreg.py:73` (muncul 2x)
- `namsniff.py:12` (muncul 2x)
- `premium.resifactory.net:77` (muncul 1x)
- `ambrowser.py:38` (muncul 1x)
- `namsniff.py:31` (muncul 1x)
- `nambrowser.py:38` (muncul 1x)
- `nexport.py:15` (muncul 1x)
- `nexport.py:21` (muncul 1x)
- `nexport.py:27` (muncul 1x)
- `mistune.py:435` (muncul 1x)
- `tpremium.resifactory.net:7777` (muncul 1x)
- `tpremium.resifactory.net:1080` (muncul 1x)

### Format user proxy yang terpakai

- `jPDZYa2fSH3jMmQN-s` (muncul 45x)
- `ipcc3tdr8d69yvbzv` (muncul 33x)
- `6pyu2taqjl` (muncul 32x)
- `jPDZYa2fSH3jMmQN` (muncul 21x)
- `ResiFactory_<id>~us~t1` (muncul 18x)
- `6pyu2taqjl-country-us` (muncul 10x)
- `jPDZYa2fSH3jMmQN[-co-CC][-s-SESSION]-type-residential` (muncul 9x)
- `ResiFactory_<id>~us~abc123` (muncul 7x)
- `ResiFactory_<id>~us~t2` (muncul 6x)
- `ResiFactory_<id>~id~mysesi1~60` (muncul 5x)
- `6pyu2taqjl-country-ID-city-bandung` (muncul 4x)
- `jPDZYa2fSH3jMmQN-type-residential` (muncul 3x)
- `ResiFactory_<id>~us~obtest01` (muncul 3x)
- `jPDZYa2fSH3jMmQN-co-US-type-residential` (muncul 3x)
- `ResiFactory_<id>~id~stk1794900938` (muncul 2x)
- `jPDZYa2fSH3jMmQN-co-US-type-res` (muncul 1x)
- `ResiFactory_<id>~id~stk1794900938-session` (muncul 1x)
- `ResiFactory_<id>~id~stk1794900938-sessid-stk1794900938` (muncul 1x)
- `ResiFactory_<id>~id~s1794900947` (muncul 1x)
- `ResiFactory_<id>~id~s1794900947-s-30` (muncul 1x)
