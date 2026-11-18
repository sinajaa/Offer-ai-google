#!/usr/bin/env python3
"""Tes ulang semua key obscurify + nomask, tulis daftar yang benar-benar bisa chat.

  python3 check_keys.py

Hasil: ob_ready.txt, nm_ready.txt (hanya key yang lolos tes chat).
"""
import concurrent.futures, json, re, time, urllib.error, urllib.request

UA = {"Content-Type": "application/json"}


def call(url, key, body=None, timeout=90):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method="POST" if data else "GET",
                                  headers={"Authorization": "Bearer " + key, **UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r), None
    except urllib.error.HTTPError as e:
        return None, f"http{e.code}"
    except Exception as e:
        return None, type(e).__name__


def obscurify():
    rows = [l.strip() for l in open("ob_accounts.txt") if l.strip()]
    seen, out = set(), []
    for r in rows:
        p = [x.strip() for x in r.split("|")]
        if len(p) < 2 or not p[1].startswith("sk-obs1_") or p[1] in seen:
            continue
        seen.add(p[1])
        out.append((p[0], p[1]))

    def one(item):
        num, key = item
        bal, err = call("https://obscurify.ai/get_user_balance", key, timeout=30)
        if err or not bal or not (bal.get("balance") or 0) > 0:
            return None
        chat, err = call("https://obscurify.ai/v1/chat/completions", key,
                         {"model": "deepseek/deepseek-v4.1-flash-1017-uncensored",
                          "messages": [{"role": "user", "content": "ok"}], "max_tokens": 5})
        return (num, key, round(bal["balance"], 4)) if chat and not err else None

    with concurrent.futures.ThreadPoolExecutor(10) as ex:
        return [x for x in ex.map(one, out) if x]


def nomask():
    keys = {}
    for f in ("nm_api_keys.txt", "nm2_api.txt", ".key_used", ".key_current"):
        try:
            txt = open(f).read()
        except FileNotFoundError:
            continue
        for m in re.finditer(r"nmk_live_[A-Za-z0-9_\-]{20,}", txt):
            keys.setdefault(m.group(0), None)
    emails = {}
    for f in ("nm_api_keys.txt", "nm2_api.txt"):
        try:
            for l in open(f):
                if "nmk_live_" in l and "|" in l:
                    p = [x.strip() for x in l.split("|")]
                    emails[p[1]] = p[0]
        except FileNotFoundError:
            pass

    def one(k):
        me, err = call("https://nomask.ai/api/v1/me", k, timeout=30)
        if err or not me:
            return None
        chat, err = call("https://nomask.ai/api/v1/chat/completions", k,
                         {"model": "deepseek_v4.1_flash_1017_uncensored",
                          "messages": [{"role": "user", "content": "ok"}], "max_tokens": 5})
        return (emails.get(k, "?"), k) if chat and not err else None

    with concurrent.futures.ThreadPoolExecutor(5) as ex:
        return [x for x in ex.map(one, keys) if x]


def write(path, header, rows, fmt):
    with open(path, "w") as f:
        f.write(f"# {header} | {time.strftime('%Y-%m-%d %H:%M')}\n")
        for r in rows:
            f.write(fmt(r) + "\n")


if __name__ == "__main__":
    ob = sorted(obscurify(), key=lambda z: -z[2])
    write("ob_ready.txt", f"obscurify — {len(ob)} key TERUJI CHAT OK, saldo ${sum(x[2] for x in ob):.2f}",
          ob, lambda z: f"{z[0]} | {z[1]} | ${z[2]:.4f}")
    print(f"obscurify : {len(ob)} key, ${sum(x[2] for x in ob):.2f}")

    nm = nomask()
    write("nm_ready.txt", f"nomask — {len(nm)} key TERUJI CHAT OK",
          nm, lambda z: f"{z[0]} | {z[1]} | deepseek_v4.1_flash_1017_uncensored")
    print(f"nomask    : {len(nm)} key")
