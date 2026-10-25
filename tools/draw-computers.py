"""Original SVG illustrations, drawn from the model references in computers.md."""
from pathlib import Path
from html import escape
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
logo=ET.parse(ROOT/'dist/assets/msx-logo.svg').getroot().find('.//{http://www.w3.org/2000/svg}path').attrib['d']
class Drawing:
 def __init__(self,title):self.s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 420" role="img" aria-label="{title}"><title>{title}</title><defs><linearGradient id="silver" x2=".2" y2="1"><stop stop-color="#d5d6d3"/><stop offset=".5" stop-color="#a4aaa9"/><stop offset="1" stop-color="#777f81"/></linearGradient><linearGradient id="graphite" x2=".3" y2="1"><stop stop-color="#55595c"/><stop offset="1" stop-color="#25292d"/></linearGradient><linearGradient id="cream" x2=".1" y2="1"><stop stop-color="#eee9d6"/><stop offset="1" stop-color="#bcb9a7"/></linearGradient><linearGradient id="bluegrey" x2=".3" y2="1"><stop stop-color="#a4afbf"/><stop offset="1" stop-color="#636f87"/></linearGradient><linearGradient id="key" x2=".1" y2="1"><stop stop-color="#e4dfc9"/><stop offset="1" stop-color="#a6a58f"/></linearGradient><linearGradient id="greykey" x2=".1" y2="1"><stop stop-color="#b1b5b1"/><stop offset="1" stop-color="#7c8585"/></linearGradient></defs><ellipse cx="450" cy="393" rx="424" ry="19" fill="#24392c" opacity=".14"/>']
 def rect(self,x,y,w,h,c,r=3,stroke=None):self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{c}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')
 def text(self,x,y,t,size=12,c='#e4e2d3',weight='400',family='Arial, sans-serif'):self.s.append(f'<text x="{x}" y="{y}" fill="{c}" font-family="{family}" font-size="{size}" font-weight="{weight}">{escape(t)}</text>')
 def line(self,x,y,x2,y2,c='#21262b',width=1):self.s.append(f'<path d="M{x} {y}H{x2}" fill="none" stroke="{c}" stroke-width="{width}"/>' if y==y2 else f'<path d="M{x} {y}L{x2} {y2}" fill="none" stroke="{c}" stroke-width="{width}"/>')
 def mark(self,x,y,w=50,c='#e7e5d7',suffix=''):
  self.s.append(f'<g transform="translate({x} {y}) scale({w/512})"><path d="{logo}" fill="{c}"/></g>')
  if suffix:self.text(x+w+1,y+w*.34,suffix,w*.36,c,'700')
 def key(self,x,y,w,h,label,dark=False,grey=False):
  c='#353b40' if dark else '#30383a';self.rect(x,y+3,w,h,'#20282c',2);self.rect(x,y,w,h,'#484e50' if dark else 'url(#greykey)' if grey else 'url(#key)',2, '#252e32' if dark else '#92968b');self.line(x+3,y+2,x+w-3,y+2,'#ffffff38');self.text(x+w/2,y+h*.62,label,8 if len(label)>4 else 10,'#ececdc' if dark else c,'500');self.s[-1]=self.s[-1].replace('<text ','<text text-anchor="middle" ')
 def row(self,x,y,w,h,labels,darkmods=True,allgrey=False):
  weights=[2 if a in ['SHIFT','RETURN','SPACE'] else 1.6 if a in ['CTRL','TAB','ESC'] else 1 for a in labels]
  if 'SPACE' in labels:weights[labels.index('SPACE')]=8
  unit=(w-4*(len(labels)-1))/sum(weights)
  for label,weight in zip(labels,weights):
   kw=unit*weight;self.key(round(x,2),y,round(kw,2),h,'' if label=='SPACE' else label,darkmods and len(label)>1 and label!='SPACE',allgrey);x+=kw+4
 def keyboard(self,x,y,w,h,darkmods=True,functionsGrey=False):
  rows=[['F1 · 6','F2 · 7','F3 · 8','F4 · 9','F5 · 10','SELECT','STOP'],['ESC','1','2','3','4','5','6','7','8','9','0','−','=','BS'],['TAB','Q','W','E','R','T','Y','U','I','O','P','[',']'],['CTRL','A','S','D','F','G','H','J','K','L',';','RETURN'],['SHIFT','Z','X','C','V','B','N','M',',','.','/','SHIFT'],['CAPS','GRAPH','SPACE','CODE']]
  kh=(h-5*6)/6
  for i,row in enumerate(rows):self.row(x,y+i*(kh+6),w,kh,row,darkmods,functionsGrey and i==0)
 def pad(self,x,y,w,red=True,cream=False):
  self.rect(x,y,w,w,'#242b2f' if not cream else '#b6b9ad',2)
  col='#3b4245' if not cream else '#cbcdbf';txt='#cf6753' if red else '#535f61'
  polys=[([(0,0),(w,0),(w*.65,w*.35),(w*.35,w*.35)],'▲',.5,.21), ([(w,0),(w,w),(w*.65,w*.65),(w*.65,w*.35)],'▶',.83,.56), ([(0,w),(w,w),(w*.65,w*.65),(w*.35,w*.65)],'▼',.5,.9), ([(0,0),(0,w),(w*.35,w*.65),(w*.35,w*.35)],'◀',.17,.56)]
  for points,label,tx,ty in polys:
   self.s.append('<polygon points="'+' '.join(f'{x+px},{y+py}' for px,py in points)+'" fill="'+col+'" stroke="#20292c" stroke-width="2"/>');self.text(x+w*tx-7,y+w*ty,label,18,txt)
  self.rect(x+w*.38,y+w*.38,w*.24,w*.24,col,1)
 def vents(self,x,y,w,h,vertical=True):
  if vertical:
   for a in range(int(x),int(x+w),8):self.rect(a,y,3,h,'#1c2733',1)
  else:
   for a in range(int(y),int(y+h),6):self.rect(x,a,w,2,'#6e756c',1)
 def save(self,name): (ROOT/'dist/assets/computers'/name).write_text(''.join(self.s)+'</svg>')
# Philips VG-8020: silver upper fascia, black cartridge lid, dark keyboard surround.
d=Drawing('Philips VG-8020 — MSX1')
d.rect(22,27,856,361,'#252c30',11,'#101b23');d.rect(22,20,856,120,'url(#silver)',8,'#616e73');d.rect(137,20,285,118,'#171b1e',1);d.text(444,55,'PHILIPS',26,'#19252d','700');d.text(319,107,'VG-8020',20,'#d35b4e','700');d.line(150,112,408,112,'#bb584e');d.text(447,101,'80K RAM   /   32K ROM',10,'#243139');d.mark(447,109,43,'#18262e');d.s.append('<path d="M66 40H90V61Q78 78 66 61Z" fill="none" stroke="#5d6a70"/>');d.text(69,49,'PHILIPS',4,'#5d6a70');d.line(70,55,86,55,'#5d6a70');d.line(70,60,86,60,'#5d6a70');d.rect(799,108,8,4,'#be5c50');d.rect(828,108,8,4,'#88a873');d.text(785,126,'POWER  CAPS',7,'#26373b');d.rect(47,150,690,211,'#151f24',3);d.keyboard(55,156,666,192);d.pad(758,236,95);d.row(752,159,104,23,['HOME','INS','DEL']);d.text(53,379,'PHILIPS PERSONAL COMPUTER',8,'#7f8989');d.save('vg-8020.svg')
# Philips VG-8235: large dark housing, raised rear body and hinged keyboard.
d=Drawing('Philips VG-8235 — MSX2')
d.rect(32,28,838,169,'#252b30',9,'#151d25');d.rect(32,18,838,149,'url(#graphite)',6,'#606b70');d.vents(66,32,170,87);d.vents(590,32,60,87);d.text(691,51,'VG-8235',23,'#e3e0d5','700');d.text(694,68,'64K ROM  ·  256K RAM',9);d.mark(694,75,47,suffix='2');d.text(692,126,'New Media Systems',13,'#cc8567','600');d.rect(48,131,807,28,'#363d41',3,'#1c252d');d.text(66,140,'RESET   POWER   CAPS   FDD BUSY',6,'#b9c1bd');d.rect(65,145,22,8,'#1b272b');
for x,c in [(108,'#b06555'),(126,'#709271'),(144,'#ab8557')]:d.rect(x,146,8,4,c,1)
d.rect(340,137,180,18,'#424b50',2,'#222b30');d.rect(868,71,9,66,'#141d26',1);d.rect(38,180,824,212,'url(#graphite)',11,'#171f25');d.rect(58,190,654,170,'#202a2e',3);d.keyboard(67,195,631,157,True,True);d.pad(744,252,91);d.row(738,196,109,22,['HOME','INS','DEL'],False,True);d.rect(319,368,257,17,'#2b3338',10,'#6b7478');d.text(69,382,'PHILIPS',11,'#cad1c9','700');d.save('vg-8235.svg')
# Sony HB-F700P: desktop system unit and physically separate full-size keyboard.
d=Drawing('Sony HB-F700P — MSX2 met los toetsenbord')
d.rect(111,28,678,124,'#b4b5a6',5,'#8a9489');d.rect(111,19,678,84,'url(#cream)',4,'#b2b7a8');d.vents(147,30,170,13,False);d.vents(147,51,170,13,False);d.vents(147,72,170,13,False);d.vents(336,30,43,55,False);d.rect(111,96,678,68,'url(#cream)',3,'#969f92');d.text(127,92,'SONY',20,'#4e5a51','700','Georgia,serif');d.rect(143,109,382,31,'#8d978b',1,'#7d8b7b');d.rect(153,120,165,9,'#45564e',1);d.rect(339,120,165,9,'#45564e',1);d.text(153,117,'1   CARTRIDGE  ·  256K RAM',6,'#e1e8d2');d.text(339,117,'2   CARTRIDGE',6,'#e1e8d2');d.rect(557,109,205,31,'#bfc2b2',2,'#a5ac9a');d.rect(568,117,182,7,'#33483c',0);d.rect(675,132,60,5,'#a1a994',0);d.text(618,105,'HB-F700P',9,'#67725e','700');d.rect(125,111,10,7,'#6eaa75');d.mark(485,146,33,'#66725f',suffix='2');d.text(571,157,'▦     ▦       ○',12,'#2a4034');d.s.append('<path d="M440 165 C410 186 510 173 456 200" fill="none" stroke="#a7ae9b" stroke-width="6"/>');d.rect(35,209,830,182,'url(#cream)',10,'#a6b0a0');d.text(57,232,'SONY',23,'#4b5b4d','700','Georgia,serif');d.text(751,229,'HiT BiT',17,'#52624f','700');d.rect(56,245,622,126,'#9da995',2);d.keyboard(64,250,605,113,False,True);d.pad(737,239,76,False,True)
for ri,row in enumerate([['7','8','9','/'],['4','5','6','*'],['1','2','3','−'],['0','.','↵','+']]):d.row(705,321+ri*15,136,12,row,False)
d.text(60,381,'HOME INTELLIGENT TERMINAL',7,'#7d8c75');d.save('hb-f700p.svg')
# Panasonic FS-A1ST: blue-grey body, raised rear fascia, gold PCM/status strip.
d=Drawing('Panasonic FS-A1ST — MSX turbo R')
d.rect(25,32,850,357,'#58657b',13,'#414e64');d.rect(25,21,850,125,'url(#bluegrey)',8,'#5e6e81');d.vents(46,26,802,21);d.text(417,66,'PERSONAL COMPUTER FS-A1ST',10,'#35455b');d.mark(687,53,64,'#2d3e52');d.text(757,73,'turbo R',16,'#34465c','700');d.rect(38,82,823,57,'#4a5670',5,'#2b3d55');d.text(58,121,'A1ST',30,'#d2b875','700');d.rect(262,94,230,28,'#3b475e',2,'#283b51');d.rect(273,99,206,6,'#151e2e',0);d.rect(430,116,42,8,'#b5b7b2',0);d.rect(522,106,316,18,'#c7ad71',4);d.text(534,119,'PCM  •••   CAPS  KANA  PAUSE  R800',9,'#333b3e','700');d.rect(45,153,664,202,'#8996a5',3);d.keyboard(53,160,646,184,False,True);d.text(55,372,'Panasonic',20,'#d1c58f','700');d.text(55,149,'WP',14,'#d6cb9c','700');d.row(727,166,126,23,['INS','DEL','HOME'],False);d.row(727,199,126,23,['7','8','9'],False);d.row(727,232,126,23,['4','5','6'],False);d.pad(745,274,98,False,True);d.rect(872,298,8,34,'#263447',1);d.text(697,387,'MSX turbo R   ·   256KB RAM',8,'#bbc7d1');d.save('fs-a1st.svg')
