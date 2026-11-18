#!/usr/bin/env python3
"""AllModels: signup -> login -> claim free credit -> ambil API key.

Kunci: token Turnstile harus dibuat DARI IP yang sama dengan submit
(TurnstileTask + proxy, bukan ProxyLess).

  python3 amreg.py            # satu akun
  python3 amreg.py --noprox   # tanpa proxy (pembanding)

Hasil -> am_accounts.txt
"""
import http.cookiejar
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from capsolve import solve_turnstile

BASE = "https://dash.allmodels.io"
SITEKEY = "0x4AAAAAAFoFe99_cOH0RnFT"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

RF_USER = "ResiFactory_<id>"
RF_PASS = "<proxy-pass>"
RF_HOST = "premium.resifactory.net"
RF_PORT = "7777"


def new_session(proxy_url=None):
    cj = http.cookiejar.CookieJar()
    if proxy_url:
        op = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy_url, "https": proxy_url}),
            urllib.request.HTTPCookieProcessor(cj))
    else:
        op = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), urllib.request.HTTPCookieProcessor(cj))
    op.addheaders = [("User-Agent", UA), ("Accept-Language", "en-US,en;q=0.9")]
    return op, cj


def call(op, path, body=None, headers=None, method=None):
    hdrs = {"Accept": "application/json", "Origin": BASE, "Referer": BASE + "/signup"}
    if body is not None:
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(body).encode() if body is not None else None,
        headers=hdrs, method=method)
    try:
        with op.open(req, timeout=60) as r:
            return r.status, r.read().decode(errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="ignore")
    except Exception as e:
        return 0, f"{type(e).__name__}: {e}"


def main():
    use_proxy = "--noprox" not in sys.argv
    sess_id = os.urandom(4).hex()
    proxy = f"http://{RF_USER}~us~{sess_id}:{RF_PASS}@{RF_HOST}:{RF_PORT}" if use_proxy else None
    proxy_arg = f"{RF_HOST}:{RF_PORT}:{RF_USER}~us~{sess_id}:{RF_PASS}" if use_proxy else None

    email = f"am{int(time.time())}@sinaja.cyou"
    pw = "Str0ng!Pass123"
    print(f"proxy : {'ya (us/' + sess_id + ')' if use_proxy else 'tidak'}")
    print(f"email : {email}")

    op, _ = new_session(proxy)

    st, txt = call(op, "/api/auth/get-session", method="GET")
    print(f"koneksi: HTTP {st}")

    print("solve Turnstile (action=signup) ...")
    try:
        tok = solve_turnstile(BASE + "/signup", SITEKEY, action="signup", proxy=proxy_arg)
    except Exception as e:
        print("SOLVER GAGAL:", e)
        return
    print(f"token : {len(tok)} char")

    st, txt = call(op, "/api/auth/sign-up/email",
                   {"email": email, "password": pw, "name": "Budi Santoso",
                    "callbackURL": "/overview"},
                   {"x-turnstile-token": tok})
    print(f"signup: HTTP {st} {txt[:160]}")
    if st != 200:
        return

    st, txt = call(op, "/api/me/balance", method="GET")
    print(f"balance: HTTP {st} {txt[:200]}")

    print("solve Turnstile (action=claim_credit) ...")
    try:
        tok2 = solve_turnstile(BASE + "/claim", SITEKEY, action="claim_credit", proxy=proxy_arg)
    except Exception as e:
        print("SOLVER GAGAL:", e)
        return
    st, txt = call(op, "/api/me/free-credits/claim",
                   {"recaptchaToken": tok2, "trigger": "auto"})
    print(f"claim  : HTTP {st} {txt[:250]}")

    st, txt = call(op, "/api/me/signup-key", method="GET")
    print(f"key    : HTTP {st} {txt[:250]}")

    with open("am_accounts.txt", "a") as f:
        f.write(json.dumps({"email": email, "pw": pw, "proxy": proxy_arg,
                            "claim": txt[:400], "ts": time.strftime("%F %T")}) + "\n")


if __name__ == "__main__":
    main()
