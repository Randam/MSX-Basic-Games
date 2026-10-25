const $ = selector => document.querySelector(selector);
const games = await fetch('games.json?v=20261025').then(r => r.json());
const models = {
  vg8020: {name:'PHILIPS',model:'VG-8020',type:'MSX1',generation:1,machine:'MSX1E',hz:'PAL / 50 Hz',ram:64,basic:'1.0',copyright:1983,image:'vg-8020.svg',alt:'Philips VG-8020: zilveren bovenkant, zwarte cartridgeklep en toetsenbordrand, lichte toetsen en rode richtingstoetsen'},
  vg8235: {name:'PHILIPS',model:'VG-8235',type:'MSX2',generation:2,machine:'MSX2E',hz:'PAL / 50 Hz',ram:256,basic:'2.0',copyright:1985,image:'vg-8235.svg',alt:'Philips VG-8235: donkere systeemkast met ventilatiesleuven, zijwaartse diskdrive en apart scharnierend toetsenbord met richtingstoetsen'},
  sony: {name:'SONY',model:'HB-F500P',type:'MSX2',generation:2,machine:'MSX2E',hz:'PAL / 50 Hz',ram:64,basic:'2.0',copyright:1985,image:'hb-f500p.svg',alt:'Sony HB-F500P: crèmekleurige losse systeemkast met cartridgekleppen en diskdrive, met los HiT BiT-toetsenbord en numeriek toetsenblok'},
  turbor: {name:'Panasonic',model:'FS-A1ST',type:'MSX turbo R',generation:4,machine:'MSXTRJ',hz:'NTSC / 60 Hz',ram:256,basic:'4.0',copyright:1990,image:'fs-a1st.svg',alt:'Panasonic FS-A1ST: blauwgrijze behuizing, diskdrive in het verhoogde achterdeel, goudkleurige PCM-statusstrip en lichte toetsen'}
};
let modelKey='vg8020', selected=games[0], running=false, powered=true, crt=true, launchedTitle='';
const currentModel=()=>models[modelKey];
const availableGames=()=>games.filter(g=>g.minimumGeneration<=currentModel().generation && (currentModel().generation!==1 || g.msx1Compatible));
function syncSelection(){
  const available=availableGames();
  if(!available.some(g=>g.id===selected.id)) selected=available[0];
  $('#selected-title').textContent=selected.title;
  $('#selected-requirement').textContent=selected.minimumGeneration===1?'MSX1':'MSX2';
  $('#start').innerHTML='Start game <span>↗</span>';
  $('#original-game-note').hidden=selected.file!=='TRONS.BAS';
  $('#original-game-note').textContent=selected.file==='TRONS.BAS'?'Let op: de oorspronkelijke muziekroutine kan een fout geven.':'';
}
function render(){
  const available=availableGames();
  const filtered=available.filter(g=>g.title.toLowerCase().includes($('#search').value.toLowerCase()));
  $('#available-count').textContent=available.length;
  $('#compatibility-note').textContent=currentModel().generation===1
    ? `${available.length} van ${games.length} games geschikt voor MSX1. De overige games zijn beschikbaar bij de MSX2-modellen. Laden gebeurt via een virtuele externe diskdrive.`
    : `Alle ${games.length} games beschikbaar op deze ${currentModel().type}.`;
  $('#game-list').replaceChildren(...filtered.map(g=>{
    const button=document.createElement('button');
    button.className='game-card'+(selected.id===g.id?' selected':'');
    button.setAttribute('aria-pressed',String(selected.id===g.id));
    button.innerHTML=`<img src="${g.image}" alt="Screenshot ${g.title}" loading="lazy"><div><strong>${g.title}</strong><small>MSX${g.minimumGeneration===1?'1':'2'} BASIC</small></div><span class="number">${selected.id===g.id?'↗':String(g.id+1).padStart(2,'0')}</span>`;
    button.onclick=()=>{selected=g;syncSelection();render()};
    return button;
  }));
  if(!filtered.length) $('#game-list').textContent='Geen passende games gevonden. Probeer een andere naam of kies een MSX2.';
}
function status(text){$('#status').lastChild.textContent=' '+text}
function start(){
  if(!availableGames().some(g=>g.id===selected.id)){syncSelection();render()}
  powered=true;running=true;launchedTitle=selected.title;
  $('#screen').classList.remove('off-screen');$('#power').setAttribute('aria-pressed','true');$('#idle').hidden=true;
  const m=currentModel(),frame=$('#emulator');frame.hidden=false;
  frame.src='emulator/index.html?'+new URLSearchParams({MACHINE:m.machine,RAMMAPPER_SIZE:String(m.ram),RAMNORMAL_SIZE:'64',DISKA_FILES_URL:'../games/'+selected.file,BASIC_RUN:selected.run,SCREEN_FULLSCREEN_MODE:'2',SCREEN_CONTROL_BAR:'0',SCREEN_CRT_SCANLINES:'0',SCREEN_FILTER_MODE:'0',AUTO_POWER_ON_DELAY:'0',CPU_SOFT_TURBO_AUTO_ON:'0'});
  status('Laden: '+selected.title+'…');$('#start').innerHTML='Opnieuw spelen <span>↗</span>';
}
window.addEventListener('message',event=>{
  if(event.origin!==location.origin||event.source!==$('#emulator').contentWindow)return;
  if(event.data?.type==='msx-ready')status(launchedTitle+' · klik in het scherm om te spelen');
  if(event.data?.type==='msx-error')status('Laden mislukt · probeer Herstart');
});
function setModel(key){
  modelKey=key;const m=currentModel();
  document.querySelectorAll('[data-model]').forEach(b=>{b.classList.toggle('selected',b.dataset.model===key);b.setAttribute('aria-pressed',String(b.dataset.model===key))});
  $('.desk').dataset.computer=key;
  $('#model-info').textContent=`${m.name.toUpperCase()} ${m.model} · ${m.type}`;
  $('#monitor-brand').textContent=m.name;
  $('#computer-art').src='assets/computers/'+m.image;$('#computer-art').alt=m.alt;
  $('#boot-generation').textContent=m.generation===1?'':m.generation===4?'turbo R':'2';
  $('#basic-version').textContent='MSX BASIC version '+m.basic;
  $('#basic-copyright').textContent='Copyright '+m.copyright+' by Microsoft';
  $('.scene-meta').lastElementChild.textContent='●  '+m.hz;
  syncSelection();render();
  if(running)start();else status('Klaar voor de start · '+m.model);
}
for(const button of document.querySelectorAll('[data-model]'))button.onclick=()=>setModel(button.dataset.model);
$('#start').onclick=start;$('#restart').onclick=start;$('#search').oninput=render;
$('#crt').onclick=()=>{crt=!crt;$('#screen').classList.toggle('crt-off',!crt);$('#crt').setAttribute('aria-pressed',String(crt));$('#crt span').textContent=crt?'CRT aan':'CRT uit'};
$('#fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('#screen').requestFullscreen()}catch{status('Volledig scherm wordt niet ondersteund in deze browser')}};
$('#power').onclick=()=>{powered=!powered;$('#screen').classList.toggle('off-screen',!powered);$('#power').setAttribute('aria-pressed',String(powered));if(!powered){$('#emulator').src='about:blank';$('#emulator').hidden=true;$('#idle').hidden=false;running=false;status('Computer uit')}else status('Klaar voor de start')};
const dialog=$('#info-dialog');
function show(kind){
  $('#dialog-content').innerHTML=kind==='help'
    ? `<p class="eyebrow">EVEN TERUG NAAR TOEN</p><h2>Klaar? Typ RUN.<br>Of klik gewoon op start.</h2><ol><li>Kies je computer. Bij de VG-8020 zie je alleen MSX1-geschikte games.</li><li>Kies een game en klik op <b>Start game</b>.</li><li>Klik in het beeldscherm om je toetsenbord te activeren. WebMSX kan een extra klik vragen voor geluid.</li><li>Volg de originele spelinstructies. Meestal gebruik je <kbd>↑ ↓ ← →</kbd>, <kbd>Spatie</kbd> en <kbd>Enter</kbd>. De toetsen verschillen per game.</li></ol><p>De VG-8020 had geen ingebouwde diskdrive. Hier laadt WebMSX de originele bestanden met een virtuele externe drive. Met <kbd>Esc</kbd> verlaat je volledig scherm.</p>`
    : `<p class="eyebrow">THE BASIC YEARS / 1992—1994</p><h2>Een toetsenbord.<br>Een hoofd vol ideeën.</h2><p>De Philips VG-8020 was mijn eerste MSX, de VG-8235 mijn tweede. De Sony HB-F500P is Bowie’s MSX; de Panasonic FS-A1ST turbo R staat nu op mijn bureau.</p><p>De gestileerde illustraties zijn getekend naar foto’s van de originele modellen. WebMSX gebruikt passende generieke MSX1-, MSX2- en turbo R-profielen met aangepast geheugen; geen modelspecifieke firmware. Turbo R kan andere timing geven dan de oorspronkelijke MSX1- en MSX2-computers.</p><p>Meer over <a href="msx-basic.html#msx-standaard"><u>de computers en hun referentiefoto’s</u></a>. De <a href="https://www.jeroenderwort.nl/wp-content/uploads/jermsx/jermsx.html" target="_blank" rel="noopener"><u>originele games</u></a> worden uitgevoerd met <a href="https://github.com/ppeccin/WebMSX" target="_blank" rel="noopener"><u>WebMSX</u></a>.</p>`;
  dialog.showModal();
}
$('#help-open').onclick=()=>show('help');$('#about-open').onclick=()=>show('about');$('#story-link').onclick=()=>show('about');$('.close-dialog').onclick=()=>dialog.close();
document.addEventListener('keydown',event=>{if(event.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)&&!dialog.open){event.preventDefault();$('#search').focus()}});
setModel('vg8020');
