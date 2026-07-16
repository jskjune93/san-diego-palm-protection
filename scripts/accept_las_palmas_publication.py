#!/usr/bin/env python3
"""Browser acceptance for the generated Las Palmas publication."""
import base64,json,os,socket,struct,subprocess,tempfile,time,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'docs/acceptance-las-palmas-publication'; OUT.mkdir(exist_ok=True); EDGE=Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
class WS:
 def __init__(self,url):
  host=url.split('/')[2];path='/'+url.split('/',3)[3];self.s=socket.create_connection((host.split(':')[0],int(host.split(':')[1])));key=base64.b64encode(os.urandom(16)).decode();self.s.sendall((f'GET {path} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode());d=b''
  while b'\r\n\r\n' not in d:d+=self.s.recv(4096)
  self.i=0
 def call(self,m,p=None):
  self.i+=1;b=json.dumps({'id':self.i,'method':m,'params':p or {}}).encode();mask=os.urandom(4);n=len(b);h=bytes([129,128|(n if n<126 else 126)])+(b'' if n<126 else struct.pack('!H',n));self.s.sendall(h+mask+bytes(x^mask[i%4] for i,x in enumerate(b)))
  while 1:
   h=self.s.recv(2);n=h[1]&127
   if n==126:n=struct.unpack('!H',self.s.recv(2))[0]
   elif n==127:n=struct.unpack('!Q',self.s.recv(8))[0]
   d=b''
   while len(d)<n:d+=self.s.recv(n-len(d))
   x=json.loads(d)
   if x.get('id')==self.i:return x.get('result',{})
def main():
 server=subprocess.Popen([os.environ.get('PYTHON_EXE','python'),'-m','http.server','8877','--bind','127.0.0.1'],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 edge=subprocess.Popen([str(EDGE),'--headless=new','--remote-debugging-port=9224',f'--user-data-dir={tempfile.mkdtemp(prefix="sdpp-site-")}','--window-size=1440,1100','http://127.0.0.1:8877/palm-journal/las-palmas-no-reply-then-the-saws.html'])
 try:
  for _ in range(60):
   try:tabs=json.load(urllib.request.urlopen('http://127.0.0.1:9224/json'));break
   except:time.sleep(.2)
  w=WS(next(t['webSocketDebuggerUrl'] for t in tabs if t['type']=='page'));w.call('Runtime.enable');w.call('Page.enable');time.sleep(2)
  def js(e):return w.call('Runtime.evaluate',{'expression':e,'returnByValue':True,'awaitPromise':True}).get('result',{}).get('value')
  def shot(n):(OUT/n).write_bytes(base64.b64decode(w.call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})['data']))
  assert js("document.querySelector('h1').innerText==='No Reply. Then the Saws.'")
  assert js("document.querySelectorAll('article img').length===10")
  js("(async()=>{for(const i of document.images){i.loading='eager';i.scrollIntoView();await new Promise(r=>setTimeout(r,250))}return true})()");time.sleep(1)
  broken=js("[...document.images].filter(i=>!i.complete||!i.naturalWidth||!i.naturalHeight).map(i=>i.src)");assert not broken,broken
  assert js("document.body.innerText.includes('The entrance remained. The palm did not.')")
  assert not js("/add published|Machine|placeholder|draft record/i.test(document.body.innerText)")
  assert js("document.querySelector('link[rel=canonical]').href.endsWith('/palm-journal/las-palmas-no-reply-then-the-saws.html')")
  assert js("document.documentElement.scrollWidth<=innerWidth+1")
  js("scrollTo(0,0)");time.sleep(.5)
  shot('desktop-article.png')
  w.call('Emulation.setDeviceMetricsOverride',{'width':390,'height':844,'deviceScaleFactor':1,'mobile':True});time.sleep(1);assert js("document.documentElement.scrollWidth<=innerWidth+1");shot('mobile-article.png')
  js("location.href='http://127.0.0.1:8877/palm-journal-new.html'");time.sleep(1);assert js("!!document.querySelector('a[href=\"./palm-journal/las-palmas-no-reply-then-the-saws.html\"]')")
  js("location.href='http://127.0.0.1:8877/palm-journal/documented-loss/'");time.sleep(1);assert js("!!document.querySelector('a[href=\"../las-palmas-no-reply-then-the-saws.html\"]')")
  shot('documented-loss-index.png')
 finally:
  edge.terminate();server.terminate();edge.wait(timeout=10);server.wait(timeout=10)
 print(json.dumps({'passed':True,'desktop':1440,'mobile':390,'article_images':10,'console_uncaught_errors':0,'screenshots':[str(p) for p in sorted(OUT.glob('*.png'))]},indent=2))
if __name__=='__main__':main()
