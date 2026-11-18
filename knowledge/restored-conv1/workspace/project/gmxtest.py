#!/usr/bin/env python3
"""Uji nyata: apakah token CaptchaFox dari capbypass diterima GMX signup.

Alur GMX (dari main.js registrasi):
  1. POST https://signup.gmx.com/account/email-registration
     header `cf-captcha-response: <token>`   <- inilah yang dites
     body  {user: {...}, mailAccount: {email}, product, ...}

  Sukses  -> 201/200 atau pesan "MTAN" (kode SMS)
  Captcha ditolak -> 400 dengan error captcha
"""
import json
import random
import string
import sys
import urllib.error
import urllib.request

from capsolve import solve_captchafox

GMX_URL = "https://signup.gmx.com/"
GMX_KEY = "sk_vKdD8WGlPF5FKpRDs1U4qTuu6Jv0w"
REG = "https://signup.gmx.com/account/email-registration"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def rand_alias(n=10):
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(n))


def post(url, body, headers, timeout=40):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode(errors="ignore")[:500]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="ignore")[:500]


def build_body(alias, password):
    return {
        "user": {
            "givenName": "Budi",
            "familyName": "Santoso",
            "gender": "MALE",
            "birthDate": "1997-03-16",
            "address": {
                "countryCode": "US",
                "region": "NY",
                "postalCode": "10001",
                "locality": "New York",
                "streetAddress": "350 5th Ave",
            },
            "credentials": {"password": password},
        },
        "mailAccount": {"email": f"{alias}@gmx.com"},
        "product": "FreeMail",
    }


def main():
    alias = "t" + rand_alias(11)
    password = "Str0ng!Pass" + rand_alias(4)
    print(f"alias: {alias}@gmx.com")

    print("minta token CaptchaFox ...")
    token = solve_captchafox(GMX_URL, GMX_KEY)
    print(f"token: {token[:40]}... ({len(token)} char)")

    headers = {
        "Content-Type": "application/vnd.ui.mam.account.creation+json",
        "Accept": "application/vnd.ui.mam.account.creation-v1+json",
        "cf-captcha-response": token,
        "User-Agent": UA,
        "Origin": "https://signup.gmx.com",
        "Referer": "https://signup.gmx.com/",
        "X-UI-APP": "oneReg/1.0.0",
        "Template-Name": "gmx",
    }
    status, text = post(REG, build_body(alias, password), headers)
    print(f"\nHTTP {status}")
    print(text)
    print("\n=== baca ===")
    if status in (200, 201):
        print("DITERIMA -> akun dibuat / lanjut MTAN")
    elif "captcha" in text.lower():
        print("CAPTCHA DITOLAK")
    else:
        print("ditolak, alasan lain (lihat body)")


if __name__ == "__main__":
    main()
