#!/usr/bin/env python3
"""Uji apakah token reCAPTCHA Enterprise (capbypass) diterima AllModels.

Endpoint anonim: POST https://dash.allmodels.io/api/free-credits/claim
  body {claimToken, recaptchaToken, trigger}  credentials:"omit"
Sitekey: 6LfevBIuAAAAABj4MatLSIOOPOFa_IBz1nG6veLh   action: claim_credit

Tujuan: membedakan 3 kemungkinan penolakan
  - captcha_failed  -> token ditolak (skor/enterprise)
  - token invalid    -> captcha LULUS, masalah di claimToken
  - sukses           -> farming jalan
"""
import json
import sys
import urllib.error
import urllib.request

from capsolve import solve_recaptcha3

SITEKEY = "6LfevBIuAAAAABj4MatLSIOOPOFa_IBz1nG6veLh"
PAGE = "https://dash.allmodels.io/claim"
API = "https://dash.allmodels.io/api/free-credits/claim"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def post(body, token):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        API,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "https://dash.allmodels.io",
            "Referer": PAGE,
            "User-Agent": UA,
            "cf-captcha-response": token,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode(errors="ignore")[:400]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="ignore")[:400]


def main():
    claim_token = sys.argv[1] if len(sys.argv) > 1 else "dummy-claim-token-000"
    print(f"claimToken: {claim_token[:30]}")

    print("minta token reCAPTCHA v3 Enterprise (action=claim_credit) ...")
    token = solve_recaptcha3(PAGE, SITEKEY, action="claim_credit", enterprise=True)
    print(f"token: {token[:45]}... ({len(token)} char)")

    for label, body in [
        ("enterprise+claimToken", {"claimToken": claim_token, "recaptchaToken": token, "trigger": "auto"}),
        ("dummy claimToken", {"claimToken": "x" * 32, "recaptchaToken": token, "trigger": "auto"}),
    ]:
        status, text = post(body, token)
        print(f"\n--- {label} -> HTTP {status}")
        print(text)


if __name__ == "__main__":
    main()
