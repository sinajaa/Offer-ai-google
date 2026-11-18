#!/usr/bin/env python3
"""Klien capbypass.pro — solver captcha cadangan.

  python3 capsolve.py balance
  python3 capsolve.py turnstile <url> <sitekey>
  python3 capsolve.py recaptcha3 <url> <sitekey> [action]
  python3 capsolve.py geetest <url> <captchaId>

Sebagai modul:
  from capsolve import solve_turnstile, solve_recaptcha3
"""
import json
import sys
import time
import urllib.error
import urllib.request

KEY = "cap_live_REDACTED"
API = "https://api.capbypass.pro"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def _post(path, payload, timeout=30):
    req = urllib.request.Request(API + path, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Accept": "application/json",
                                          "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            raise RuntimeError(f"HTTP {e.code}: {body[:120]}")


def balance():
    return _post("/getBalance", {"clientKey": KEY}).get("balance")


def _run(task, timeout=180, poll=3):
    res = _post("/createTask", {"clientKey": KEY, "task": task})
    if res.get("errorId"):
        raise RuntimeError(f"createTask: {res.get('errorCode')} {res.get('errorDescription')}")
    tid = res["taskId"]
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(poll)
        r = _post("/getTaskResult", {"clientKey": KEY, "taskId": tid})
        if r.get("status") == "ready":
            return r["solution"]
        if r.get("errorId"):
            raise RuntimeError(f"{r.get('errorCode')}: {r.get('errorDescription')}")
    raise TimeoutError(f"task {tid} belum selesai dalam {timeout}s")


def solve_turnstile(url, sitekey, **kw):
    s = _run({"type": "TurnstileTaskProxyLess", "websiteURL": url, "websiteKey": sitekey}, **kw)
    return s["token"]


def solve_recaptcha3(url, sitekey, action="login", enterprise=False, **kw):
    t = "ReCaptchaV3EnterpriseTaskProxyLess" if enterprise else "ReCaptchaV3TaskProxyLess"
    s = _run({"type": t, "websiteURL": url, "websiteKey": sitekey, "pageAction": action}, **kw)
    return s["gRecaptchaResponse"]


def solve_geetest(url, captcha_id, **kw):
    return _run({"type": "GeetestTaskProxyLess", "websiteURL": url, "captchaId": captcha_id}, **kw)


def solve_captchafox(url, sitekey, **kw):
    """sitekey format `sk_...`. GMX: sk_vKdD8WGlPF5FKpRDs1U4qTuu6Jv0w"""
    s = _run({"type": "CaptchaFoxTaskProxyLess", "websiteURL": url, "websiteKey": sitekey}, **kw)
    return s["token"] if isinstance(s.get("solution"), dict) is False else s["solution"]["token"]


def solve_aws_waf(url, **kw):
    """Balikkan dict lengkap: token, cookie, captchaVoucher, userAgent (semua dibutuhkan)."""
    return _run({"type": "AntiAwsWafTaskProxyLess", "websiteURL": url}, **kw)


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] == "balance":
        print("saldo: $%s" % balance())
    elif a[0] == "turnstile":
        print(solve_turnstile(a[1], a[2]))
    elif a[0] == "recaptcha3":
        print(solve_recaptcha3(a[1], a[2], a[3] if len(a) > 3 else "login"))
    elif a[0] == "geetest":
        print(json.dumps(solve_geetest(a[1], a[2])))
    elif a[0] == "captchafox":
        print(solve_captchafox(a[1], a[2]))
    elif a[0] == "awswaf":
        print(json.dumps(solve_aws_waf(a[1]), indent=1)[:400])
    else:
        print(__doc__)
