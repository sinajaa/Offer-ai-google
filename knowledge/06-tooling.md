# 06 — Tooling untuk kerja tahan-banting

## Masalah yang diselesaikan
Sandbox bisa hilang kapan saja (idle reap / OOM / redeploy) dan chat bisa kena limit konteks.
Solusinya: state hidup di luar chat dan di luar sandbox.

## 1. autosave.sh
Commit + push + zip tiap N menit.

```bash
cd /workspace/project/<repo>
nohup /workspace/project/durable/autosave.sh 5 > /workspace/autosave.log 2>&1 &
```

- push ke `origin` branch aktif, retry 3x
- zip cadangan di `/workspace/backup`, simpan 20 terakhir
- aman dihentikan kapan saja (`pkill -f autosave.sh`)

## 2. rebuild_from_conversation.py
Bangun ulang file dari export conversation OpenHands (file JSON atau folder event).

```bash
python3 rebuild_from_conversation.py conversation.json -o restored/
python3 rebuild_from_conversation.py raw/drive-1467 -o restored-conv1/
```

- mendukung `create` / `write` / `str_replace` / `insert`
- membaca argumen tool call yang berbentuk string JSON
- hasil = kondisi terakhir menurut riwayat tool call (bukan snapshot disk)

## 3. Monitor offer (GitHub Actions)
Repo `sinajaa/Offer-ai-googl`:
- `watch.py` — cek hash token, repo baru, issue
- `.github/workflows/watch.yml` — cron 20 menit + deploy Pages
- `docs/index.html` — dashboard statis

## 4. HANDOVER.md
Template 7 bagian (status, repo, cara jalan, selesai, berikutnya, keputusan, jebakan).
Tempel di chat baru supaya konteks pulih dalam 30 detik.

## Protokol lanjut-kerja (wajib)

1. Setiap milestone: `git commit` + update `HANDOVER.md`/`STATE.json`.
2. Sebelum langkah besar (refactor/build): commit checkpoint.
3. Chat mati / sandbox mati → buka chat baru, tempel `RESUME_PROMPT.md`, lanjut.
4. Jangan andalkan ingatan chat untuk isi file; andalkan repo.
