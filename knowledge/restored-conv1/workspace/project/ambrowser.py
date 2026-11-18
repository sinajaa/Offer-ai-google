#!/usr/bin/env python3
"""AllModels signup lewat browser + proxy sticky, token dari capbypass (proxy sama).

Urutan:
  1. solve Turnstile via proxy (TurnstileTask, action=signup)
  2. buka halaman signup lewat proxy yang SAMA
  3. verifikasi IP browser == IP yang kita harapkan
  4. kirim signup via fetch di dalam halaman (cookie + origin asli)

  python3 ambrowser.py
"""
import json
import os
import time

from playwright.sync_api import sync_playwright

from capsolve import solve_turnstile

BASE = "https://dash.allmodels.io"
SITEKEY = "0x4AAAAAAFoFe99_cOH0RnFT"
PX_USER = "jPDZYa2fSH3jMmQN"
PX_PASS = "bHaUJVMb4cPlQZOL"
PX_HOST = "pg.proxi.es"
PX_PORT = "20000"


def proxy_for(sess):
    user = f"{PX_USER}-s-{sess}-co-US-type-residential"
    url = f"http://{user}:{PX_PASS}@{PX_HOST}:{PX_PORT}"
    arg = f"{PX_HOST}:{PX_PORT}:{user}:{PX_PASS}"
    return user, url, arg


def main():
    sess = "am" + os.urandom(3).hex()
    user, px_url, px_arg = proxy_for(sess)
    email = f"am{int(time.time())}@sinaja.cyou"
    print(f"sesi proxy: {sess}  email: {email}")

    print("1) solve Turnstile via proxy ...")
    tok = solve_turnstile(BASE + "/signup", SITEKEY, action="signup", proxy=px_arg)
    print(f"   token {len(tok)} char")

    with sync_playwright() as p:
        b = p.chromium.launch(headless=False, args=["--no-sandbox"])
        ctx = b.new_context(proxy={"server": f"http://{PX_HOST}:{PX_PORT}",
                                    "username": user, "password": PX_PASS})
        pg = ctx.new_page()
        print("2) buka halaman signup lewat proxy ...")
        pg.goto(BASE + "/signup", wait_until="domcontentloaded")
        pg.wait_for_timeout(4000)
        ip = pg.evaluate("fetch('https://api.ipify.org').then(r=>r.text())")
        print(f"   IP browser: {ip}")

        print("3) submit signup ...")
        res = pg.evaluate("""async ({tok,email})=>{
          const r=await fetch('/api/auth/sign-up/email',{method:'POST',
            headers:{'content-type':'application/json','x-turnstile-token':tok},
            body:JSON.stringify({email,password:'Str0ng!Pass123',name:'Budi Santoso',
                                 callbackURL:'/overview'}),credentials:'include'});
          return {status:r.status, body:(await r.text()).slice(0,300)};
        }""", {"tok": tok, "email": email})
        print("   ->", json.dumps(res, ensure_ascii=False)[:300])

        if res["status"] == 200:
            for path, body in [("/api/me/balance", None)]:
                r2 = pg.evaluate("""async (p)=>{const r=await fetch(p,{credentials:'include'});
                  return {s:r.status,t:(await r.text()).slice(0,300)};}""", path)
                print(f"   {path} -> {r2['s']} {r2['t'][:200]}")
            with open("am_accounts.txt", "a") as f:
                f.write(json.dumps({"email": email, "pw": "Str0ng!Pass123",
                                    "sess": sess, "ip": ip,
                                    "ts": time.strftime("%F %T")}) + "\n")
        b.close()


if __name__ == "__main__":
    main()
