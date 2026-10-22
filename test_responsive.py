from pathlib import Path
import asyncio, json
from playwright.async_api import async_playwright
HTML=Path('/mnt/data/sawit-panic-v5.7-creator-credit/index.html').read_text()
OUT=Path('/mnt/data/sawit-panic-v5.7-creator-credit')
SIZES=[(360,640),(375,667),(390,844),(412,915),(540,960)]
def overlap(a,b):
 x=max(0,min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x']))
 y=max(0,min(a['y']+a['height'],b['y']+b['height'])-max(a['y'],b['y']))
 return round(x*y,2)
async def main():
 results=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
  for w,h in SIZES:
   page=await browser.new_page(viewport={'width':w,'height':h},device_scale_factor=1)
   errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
   await page.set_content(HTML,wait_until='domcontentloaded',timeout=60000)
   await page.wait_for_timeout(1700)
   creator=page.locator('#menuCreatorCredit')
   menu=page.locator('#menu')
   phone=page.locator('#phone')
   rect=await creator.bounding_box()
   phone_rect=await phone.bounding_box()
   menu_rect=await menu.bounding_box()
   buttons={}
   overlaps={}
   for k in ['menuPlay','menuTutorial','menuBoard','menuSettings','menuRecordBadge','menuSound','menuSettingsTop']:
    b=await page.locator('#'+k).bounding_box()
    buttons[k]=b
    overlaps[k]=overlap(rect,b)
   attrs=await creator.evaluate('(el)=>({pointer:getComputedStyle(el).pointerEvents,role:el.getAttribute("role"),label:el.getAttribute("aria-label"),actualText:el.textContent,visibility:getComputedStyle(el).visibility})')
   stage_aspect=await phone.evaluate('(el)=>{let b=el.getBoundingClientRect();return b.width/b.height}')
   assert abs(stage_aspect-9/16)<.001,(w,h,stage_aspect)
   assert rect['x']>=menu_rect['x'] and rect['x']+rect['width']<=menu_rect['x']+menu_rect['width']
   assert rect['y']>=menu_rect['y'] and rect['y']+rect['height']<=menu_rect['y']+menu_rect['height']
   assert max(overlaps.values())==0,(w,h,overlaps)
   assert attrs['pointer']=='none'
   assert 'DEVELOPED BY' in attrs['actualText'] and 'nugrohoiif' in attrs['actualText']
   assert not errors,(w,h,errors)
   await page.screenshot(path=str(OUT/f'menu-{w}x{h}.png'),animations='disabled')
   # Confirm previously approved menu links still work.
   await page.locator('#menuTutorial').click()
   modal_state=await page.evaluate('''() => ({modals: [...document.querySelectorAll('.modal')].filter(e=>!e.hidden).map(e=>e.id),menuHidden:document.querySelector('#menu').hidden})''')
   results.append({'viewport':f'{w}x{h}','creatorBounds':rect,'stageBounds':phone_rect,'overlaps':overlaps,'errors':errors,'afterTutorial':modal_state})
   print('PASSED',w,h,'creator at',tuple(round(rect[k],1) for k in ['x','y','width','height']),'Tutorial',modal_state)
   await page.close()
  # Separate play flow
  page=await browser.new_page(viewport={'width':390,'height':844})
  errors=[];page.on('pageerror',lambda e: errors.append(str(e)))
  await page.set_content(HTML,wait_until='domcontentloaded',timeout=60000)
  await page.locator('#menuPlay').click()
  await page.wait_for_timeout(600)
  print('after play menu/game hidden',await page.locator('#menu').is_hidden(),await page.locator('#game').is_visible(),'error count',len(errors))
  assert await page.locator('#game').is_visible()
  assert await page.locator('#menu').is_hidden()
  assert not errors,errors
  await page.close()
  await browser.close()
 (OUT/'test_results.json').write_text(json.dumps(results,indent=2))
asyncio.run(main())
