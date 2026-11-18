#!/usr/bin/env python3
"""Sadap request signup AllModels asli via Playwright (headless).

Tujuan: lihat header & body persis yang dikirim browser, terutama
header token Turnstile. Jalankan: python3 amsniff.py
"""
import json
import time

from playwright.sync_api import sync_playwright

EMAIL = f"amsniff{int(time.time())}@sinaja.cyou"
PASSWORD = "Str0ng!Pass123"


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(viewport={"width": 1280, "height": 900})
        page = ctx.new_page()
        page.goto("https://dash.allmodels.io/signup", wait_until="networkidle")

        page.fill('input[placeholder="Ada Lovelace"]', "Budi Santoso")
        page.fill('input[placeholder="ada@company.com"]', EMAIL)
        page.fill('input[placeholder="At least 8 characters"]', PASSWORD)
        page.fill('input[placeholder="Re-enter your password"]', PASSWORD)

        page.wait_for_timeout(3000)
        print("tombol:", [t.inner_text() for t in page.query_selector_all("button")][:8])

        with page.expect_request("**/api/auth/sign-up/email", timeout=25000) as info:
            page.click('button[type="submit"], button:has-text("Create account"), button:has-text("Sign up")')
        req = info.value
        print("\n=== URL:", req.url)
        print("=== METHOD:", req.method)
        print("=== HEADERS:")
        for k, v in req.headers.items():
            if k.lower() in ("cookie", "authorization"):
                print(f"  {k}: <{len(v)} chars>")
            else:
                print(f"  {k}: {v[:110]}")
        print("=== BODY:", (req.post_data or "")[:400])

        resp = req.response()
        if resp:
            print("=== RESP:", resp.status, resp.text()[:300])
        print("EMAIL:", EMAIL)
        b.close()


if __name__ == "__main__":
    main()
