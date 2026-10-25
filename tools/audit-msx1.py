import subprocess,concurrent.futures,pathlib,json,zipfile,re,tempfile,os
root=pathlib.Path(__file__).resolve().parents[1]
workspace=tempfile.TemporaryDirectory(prefix='msx1-audit-');out=pathlib.Path(workspace.name)
exe=os.environ.get('OPENMSX_BIN','/Applications/openMSX.app/Contents/MacOS/openmsx')
games=json.loads((root/'dist/games.json').read_text())
def audit(g):
 d=out/str(g['id']);d.mkdir(exist_ok=True);game=root/'dist/games'/g['file']
 if game.suffix=='.zip':zipfile.ZipFile(game).extractall(d)
 else:(d/g['file']).write_bytes(game.read_bytes())
 script=out/(str(g['id'])+'.tcl');script.write_text(f'''set renderer none
set throttle off
set sound_driver null
diska {{{d}}}
set power on
after time 3 {{type_via_keybuf "\\r"}}
after time 5 {{type_via_keybuf "RUN\\\"{g['run']}\\\"\\r"}}
proc capture {{name}} {{
 set f [open "{out}/{g['id']}-$name.vram" wb]
 fconfigure $f -translation binary
 puts -nonewline $f [debug read_block VRAM 0 16384]
 close $f
}}
after time 25 {{capture title}}
after time 26 {{type_via_keybuf "N"}}
after time 40 {{type_via_keybuf " "}}
after time 55 {{capture play;exit}}
''')
 p=subprocess.run([exe,'-machine','Philips_VG_8020','-ext','Philips_VY_0010','-script',str(script)],capture_output=True,timeout=120)
 result={'id':g['id'],'title':g['title'],'errors':[],'screenSamples':[]}
 for phase in ['title','play']:
  f=out/f'{g["id"]}-{phase}.vram'
  if not f.exists():result['errors'].append('Missing runtime capture');continue
  b=f.read_bytes();text=''.join(chr(c) if 32<=c<127 else ' ' for c in b)
  errors=re.findall(r'.{0,25}(?:error in|Out of memory|Illegal function call|Syntax error|Undefined line number|Type mismatch|Out of DATA|Bad file name|File not found|Subscript out of range).{0,40}',text,re.I)
  result['errors']+=errors
  result['screenSamples'].append({'phase':phase,'text0':text[:960].strip(),'text1':text[0x1800:0x1b00].strip()})
 return result
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for r in pool.map(audit,games):results.append(r);print(r['title'],r['errors'],flush=True)
(root/'tools/compatibility/runtime-msx1.json').write_text(json.dumps(results,indent=2,ensure_ascii=False))
