import sys, re, urllib.parse, time
sys.path.insert(0,"/workspace/project/ultra")
from common import *
from playwright.sync_api import sync_playwright
JSH="m;/_/scs/abc-static/_/js/k=gapi.lb.en.smUXTMp7CeY.O/d=1/rs=AHpOoo_-UMASGI-dbLvJPxfO6N46l3l46A/m=__features__"
with sync_playwright() as p:
    ctx=launch(p); page=ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("file:///workspace/project/ultra/tool.html", wait_until="commit"); time.sleep(2)
    u20=page.evaluate("buildUrl('20tb', false)")
    u30=page.evaluate("buildUrl('30tb', false)")
    fixed=re.sub(r"&jsh=[^&]*", "&jsh="+urllib.parse.quote(JSH,safe=""), u20)
    open("/workspace/project/ultra/link_ultra20tb.txt","w").write(fixed)
    open("/workspace/project/ultra/link_ultra30tb.txt","w").write(u30)
    print("len:", len(fixed), len(u30))
    print("NO-GAPI PREFIX:", fixed.split("&usegapi=1")[0][:120])
    ctx.close()
