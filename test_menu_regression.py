from pathlib import Path
import asyncio, re
from playwright.async_api import async_playwright
old=Path('/mnt/data/sawit-panic-v5.6-balancing-bonus/index.html').read_text()
new=Path('/mnt/data/sawit-panic-v5.7-creator-credit/index.html').read_text()
# Source preservation: remove precisely the v5.7 additions and title; ensure full byte-equivalence.
stripped=re.sub(r'\n/\* v5\.7 Creator Signature:.*?(?=</style>)','',new,flags=re.S)
stripped=re.sub(r'<div id="menuCreatorCredit".*?</div>\n','',stripped,count=1)
stripped=stripped.replace('<title>SAWIT PANIC! — v5.7 Creator Credit</title>','<title>SAWIT PANIC! — v5.1 Menu Rekor</title>')
assert stripped == old+'\n' or stripped == old,('source mismatch',len(stripped),len(old))
print('PASS: full baseline source unchanged after excluding credit additions and page title')
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  for name in ['menuRecordBadge','menuTutorial','menuBoard','menuSettings','menuSound','menuSettingsTop','menuPlay']:
   page=await browser.new_page(viewport={'width':390,'height':844})
   errors=[]
   page.on('pageerror',lambda e: errors.append(str(e)))
   await page.set_content(new,wait_until='domcontentloaded',timeout=60000)
   await page.locator('#'+name).click(timeout=15000)
   await page.wait_for_timeout(80)
   active=await page.locator('.modal:not([hidden])').count()
   menu_visible=await page.locator('#menu').is_visible()
   game_visible=await page.locator('#game').is_visible()
   assert not errors,(name,errors)
   if name=='menuPlay':assert game_visible and not menu_visible
   if name in ['menuTutorial','menuBoard','menuSettings','menuSettingsTop','menuRecordBadge']:assert active>=1,(name,active)
   print('PASS',name,'modal',active,'game visible',game_visible)
   await page.close()
  page=await browser.new_page(viewport={'width':390,'height':844},reduced_motion='reduce')
  await page.set_content(new,wait_until='domcontentloaded',timeout=60000)
  anim=await page.locator('#menuCreatorCredit').evaluate('(el)=>getComputedStyle(el).animationName')
  assert anim=='none',anim
  print('PASS reduced motion prevents creator credit animation')
  await page.close()
  await browser.close()
asyncio.run(main())
