#!/usr/bin/env python3
"""Monitor offer Google AI Ultra / AI Pro free trial (link tokenized Play 'ear').

Sinyal yang dipantau:
1. Token offer di repo sumber (kalau token berubah, offer dibuka ulang).
2. Repo lain yang memuat SKU yang sama (klon baru biasanya bawa token baru).
3. Issue baru yang berbau "sudah buka lagi".
"""
import datetime
import hashlib
import json
import os
import pathlib
import re
import urllib.request

REPO = "gylive/google-ultra"
SKU = "g1.play.20tb"
BASELINE = {"88e273bb69", "12d4d4c791"}
LIVE_KW = ("又开", "复活", "恢复", "回来了", "可用", "又可以", "working again", "is back", "reopened")

TG_TOKEN = os.environ.get("TG_TOKEN", "")
TG_CHAT = os.environ.get("TG_CHAT", "")
GH_TOKEN = os.environ.get("GH_TOKEN", "")

DOCS = pathlib.Path("docs")
STATUS = DOCS / "status.json"


def http(url, headers=None, timeout=30):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "ignore")


def gh(path):
    headers = {"Accept": "application/vnd.github+json"}
    if GH_TOKEN:
        headers["Authorization"] = "Bearer " + GH_TOKEN
    return json.loads(http("https://api.github.com" + path, headers))


def token_hashes():
    try:
        raw = http(f"https://raw.githubusercontent.com/{REPO}/main/web/index.html")
    except Exception as e:
        return None, f"gagal baca repo: {e}"
    tokens = re.findall(r'token:\s*"([^"]{20,})"', raw)
    return {hashlib.sha1(t.encode()).hexdigest()[:10] for t in tokens}, None


def repo_tokens(full_name):
    for path in ("web/index.html", "web/en.html"):
        try:
            raw = http(f"https://raw.githubusercontent.com/{full_name}/main/{path}")
        except Exception:
            continue
        tokens = re.findall(r'token:\s*"([^"]{20,})"', raw)
        if tokens:
            return {hashlib.sha1(t.encode()).hexdigest()[:10] for t in tokens}
    return set()


def new_repos(known):
    """Repo yang belum pernah dilihat; hanya dianggap sinyal kalau tokennya baru."""
    try:
        data = gh(f"/search/code?q=%22{SKU}%22&per_page=30")
    except Exception as e:
        return [], [], f"code search gagal: {e}"
    names = {item["repository"]["full_name"] for item in data.get("items", [])}
    unseen = sorted(names - known)
    fresh, all_seen = [], set(names)
    for name in unseen:
        hashes = repo_tokens(name)
        if hashes - BASELINE:
            fresh.append(name)
    return fresh, sorted(all_seen), None


def issues():
    try:
        data = gh(f"/repos/{REPO}/issues?state=all&sort=created&direction=desc&per_page=10")
    except Exception as e:
        return [], f"issue gagal: {e}"
    return [
        {"n": i["number"], "title": i["title"][:100], "at": i["created_at"][:16]}
        for i in data
        if "pull_request" not in i
    ], None


def notify(text):
    if not (TG_TOKEN and TG_CHAT):
        return
    try:
        payload = json.dumps({"chat_id": TG_CHAT, "text": text}).encode()
        req = urllib.request.Request(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=20).read()
    except Exception as e:
        print("telegram gagal:", e)


def render(hist):
    last = hist.get("last", {})
    alive = last.get("verdict") == "ALIVE"
    color = "#7ee2a8" if alive else "#f28b82"
    headline = "OFFER KEMUNGKINAN DIBUKA LAGI" if alive else "BELUM ADA OFFER"

    rows = ""
    for c in hist.get("checks", [])[:40]:
        c_color = "#7ee2a8" if c["verdict"] == "ALIVE" else "#f28b82"
        reason = "; ".join(c.get("reason") or []) or "—"
        rows += (
            f"<tr><td>{c['at'][:16].replace('T', ' ')}</td>"
            f"<td style='color:{c_color};font-weight:600'>{c['verdict']}</td>"
            f"<td>{reason}</td></tr>"
        )

    issue_items = "".join(
        f"<li>#{i['n']} · {i['at'][:16]} — {i['title']}</li>" for i in last.get("issues", [])[:6]
    ) or "<li>—</li>"

    reasons = "".join(
        f"<li>{r}</li>" for r in (last.get("reason") or ["tidak ada perubahan token, repo, atau issue"])
    )

    return f"""<!doctype html><html lang="id"><meta charset="utf-8">
<meta http-equiv="refresh" content="120">
<title>Monitor Offer Google AI Ultra/Pro</title>
<style>
body{{background:#0f1115;color:#e8eaed;font:15px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:28px}}
h1{{font-size:20px;margin:0 0 4px}} .sub{{color:#9aa0a6;font-size:13px;margin-bottom:18px}}
.card{{background:#171a21;border:1px solid #262b36;border-radius:12px;padding:16px;margin-bottom:14px}}
.badge{{display:inline-block;padding:4px 10px;border-radius:99px;font-weight:700;font-size:13px;
background:{color}22;color:{color};border:1px solid {color}55;margin-bottom:8px}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid #232833}}
th{{color:#9aa0a6;font-weight:600}} ul{{margin:6px 0 0 18px;padding:0}}
code{{background:#0c0e12;padding:2px 6px;border-radius:6px;font-size:12px}}
a{{color:#8ab4f8}}
</style>
<h1>Monitor Offer Google AI Ultra / Pro</h1>
<div class="sub">Dicek otomatis tiap 20 menit lewat GitHub Actions. Halaman refresh sendiri tiap 2 menit.</div>
<div class="card"><div class="badge">{headline}</div>
<div>Pengecekan terakhir: <code>{last.get('at', '—')}</code></div>
<div>Hash token terbaca: <code>{', '.join(last.get('tokens') or []) or '—'}</code></div></div>
<div class="card"><b>Kenapa statusnya begitu</b><ul>{reasons}</ul></div>
<div class="card"><b>Issue terbaru di repo sumber</b><ul>{issue_items}</ul></div>
<div class="card"><b>Riwayat 40 pengecekan</b>
<table><tr><th>Waktu (UTC)</th><th>Status</th><th>Alasan</th></tr>{rows}</table></div>
<div class="card"><b>Kalau muncul ALIVE</b><br>
Buka <a href="https://github.com/gylive/google-ultra">repo sumber</a>, lalu
<a href="https://gylive.github.io/google-ultra/web/">versi web-nya</a> dengan akun Google + metode bayar.
Konfirmasi harga harus $0 sebelum menekan subscribe.</div>
</html>"""


def main():
    now = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    hist = json.loads(STATUS.read_text()) if STATUS.exists() else {"checks": []}
    known_repos = set(hist.get("known_repos", []))

    hashes, tok_err = token_hashes()
    fresh_repos, seen_repos, repo_err = new_repos(known_repos)
    issue_list, issue_err = issues()

    new_token = bool(hashes and (hashes - BASELINE))
    live_issues = [
        i for i in issue_list if any(k.lower() in i["title"].lower() for k in LIVE_KW)
    ]

    reasons = []
    if new_token:
        reasons.append("hash token berubah: " + ", ".join(sorted(hashes - BASELINE)))
    if fresh_repos:
        reasons.append("repo baru memuat SKU: " + ", ".join(fresh_repos[:3]))
    if live_issues:
        reasons.append("issue berbunyi buka lagi: #" + ", #".join(str(i["n"]) for i in live_issues[:3]))

    entry = {
        "at": now,
        "verdict": "ALIVE" if (new_token or fresh_repos or live_issues) else "DEAD",
        "reason": reasons,
        "tokens": sorted(hashes or []),
        "new_repos": fresh_repos,
        "issues": issue_list[:6],
        "errors": [e for e in (tok_err, repo_err, issue_err) if e],
    }

    hist["checks"] = ([entry] + hist.get("checks", []))[:200]
    hist["known_repos"] = sorted(known_repos | set(seen_repos) | {REPO})
    hist["last"] = entry

    DOCS.mkdir(exist_ok=True)
    STATUS.write_text(json.dumps(hist, indent=1, ensure_ascii=False))
    (DOCS / "index.html").write_text(render(hist), encoding="utf-8")

    previous = hist["checks"][1]["verdict"] if len(hist["checks"]) > 1 else None
    if entry["verdict"] == "ALIVE" and previous != "ALIVE":
        notify("Offer Google AI kemungkinan DIBUKA LAGI\n" + "; ".join(reasons) + f"\n{now}")

    print(json.dumps(entry, ensure_ascii=False))


if __name__ == "__main__":
    main()
