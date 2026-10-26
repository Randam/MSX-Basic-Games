import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {readFileSync} from 'node:fs';
const source = readFileSync(new URL('../dist/analytics.js', import.meta.url), 'utf8');
function setup({saved=null, hostname='msxbasic.nl', blockedStorage=false}={}) {
  const scripts=[], cookies=[], documentEvents={}, windowEvents={}, stored=[];
  let reloads=0;
  const elements=[];
  const makeElement=()=>({hidden:false,dataset:{},setAttribute(){},addEventListener(type,fn){this[type]=fn;},querySelector(){return {focus(){}};}});
  const document={referrer:'https://example.org/source?private=secret#hash',createElement:makeElement,head:{append(tag){scripts.push(tag);}},body:{append(node){elements.push(node);}},addEventListener(type,fn){documentEvents[type]=fn;}};
  Object.defineProperty(document,'cookie',{get:()=> '_ga=123; _ga_0LHYE5QJ2D=456; unrelated=keep',set:value=>cookies.push(value)});
  const location={hostname,href:'https://'+hostname+'/index.html?secret=yes#collectie',reload(){reloads++;}};
  const window={addEventListener(type,fn){windowEvents[type]=fn;}};
  const localStorage={getItem(){if(blockedStorage)throw Error('blocked');return saved?JSON.stringify(saved):null;},setItem(k,v){if(blockedStorage)throw Error('blocked');stored.push(JSON.parse(v));}};
  vm.runInNewContext(source,{window,document,location,localStorage,Date,URL});
  const banner=elements[0];
  const choose=choice=>banner.click({target:{closest:()=>({dataset:{choice}})}});
  const game=()=>documentEvents['msx-game-start']({detail:{game:'Airplane',computer:'VG-8020'}});
  return {window,scripts,banner,choose,game,cookies,stored,get reloads(){return reloads;}};
}
const fresh=choice=>({choice,updatedAt:Date.now()});
test('no Analytics tag or event before consent, or after refusing',()=>{
 const s=setup();assert.equal(s.banner.hidden,false);s.game();assert.equal(s.scripts.length,0);assert.equal(s.window.gtag,undefined);s.choose('denied');assert.equal(s.scripts.length,0);assert.equal(s.banner.hidden,true);assert.equal(s.stored[0].choice,'denied');
});
test('consent loads once, strips sensitive URL parts and keeps all advertising consent denied',()=>{
 const s=setup();s.choose('granted');s.choose('granted');assert.equal(s.scripts.length,1);assert.match(s.scripts[0].src,/G-0LHYE5QJ2D/);
 const events=s.window.dataLayer.map(args=>Array.from(args));
 const config=events.find(e=>e[0]==='config')[2];assert.equal(config.page_location,'https://msxbasic.nl/index.html');assert.equal(config.page_referrer,'https://example.org/source');assert.equal(config.allow_google_signals,false);
 const consent=events.find(e=>e[0]==='consent'&&e[1]==='update')[2];assert.equal(consent.analytics_storage,'granted');for(const k of ['ad_storage','ad_user_data','ad_personalization'])assert.equal(consent[k],'denied');
 s.game();assert.equal(s.window.dataLayer.at(-1)[1],'game_start');
});
test('valid consent is remembered; expired choice asks again; previews never send Analytics',()=>{
 assert.equal(setup({saved:fresh('granted')}).scripts.length,1);
 assert.equal(setup({saved:fresh('denied')}).scripts.length,0);
 const old=setup({saved:{choice:'granted',updatedAt:0}});assert.equal(old.banner.hidden,false);assert.equal(old.scripts.length,0);
 const preview=setup({hostname:'localhost'});preview.choose('granted');assert.equal(preview.scripts.length,0);
});
test('withdrawal disables tracking, clears only Analytics cookies and unloads the tag',()=>{
 const s=setup({saved:fresh('granted')});s.choose('denied');assert.equal(s.window['ga-disable-G-0LHYE5QJ2D'],true);assert.equal(s.reloads,1);assert.ok(s.cookies.some(c=>c.startsWith('_ga=')));assert.ok(s.cookies.every(c=>!c.startsWith('unrelated=')));
 const before=s.window.dataLayer.length;s.game();assert.equal(s.window.dataLayer.length,before);
});
test('blocked storage does not block consent or the site',()=>{
 const s=setup({blockedStorage:true});assert.equal(s.banner.hidden,false);s.choose('granted');assert.equal(s.scripts.length,1);
});
