const demo = document.querySelector('#basic-demo');
const idle = document.querySelector('#demo-idle');
const status = document.querySelector('#demo-status');
const run = document.querySelector('#run-listing');
const stop = document.querySelector('#stop-listing');
run.addEventListener('click', () => {
  idle.hidden = true;
  demo.hidden = false;
  stop.hidden = false;
  demo.src = 'emulator/index.html?' + new URLSearchParams({
    MACHINE: 'MSX2E', DISKA_FILES_URL: '../examples/HALLO.BAS', BASIC_RUN: 'HALLO.BAS',
    SCREEN_FULLSCREEN_MODE: '2', SCREEN_CONTROL_BAR: '0', SCREEN_FILTER_MODE: '0',
    SCREEN_CRT_SCANLINES: '0', AUTO_POWER_ON_DELAY: '0'
  });
  status.textContent = 'MSX start op…';
  run.textContent = 'Opnieuw starten ↗';
});
stop.addEventListener('click', () => {
  demo.src = 'about:blank';
  demo.hidden = true;
  idle.hidden = false;
  stop.hidden = true;
  status.textContent = 'MSX2 · WebMSX';
  run.textContent = 'Start dit programma ↗';
});
window.addEventListener('message', event => {
  if (event.origin !== location.origin || event.source !== demo.contentWindow) return;
  if (event.data?.type === 'msx-ready') status.textContent = 'Emulator geladen · de MSX start de listing';
  if (event.data?.type === 'msx-error') status.textContent = 'Laden mislukt · probeer opnieuw te starten';
});
document.querySelector('#copy-listing').addEventListener('click', async () => {
  const message = document.querySelector('#copy-status');
  try {
    await navigator.clipboard.writeText(document.querySelector('#basic-listing').textContent);
    message.textContent = 'Code gekopieerd. Je kunt de listing nu bewaren of aanpassen.';
  } catch {
    message.textContent = 'Kopiëren is niet beschikbaar. Selecteer de code hierboven of download het .BAS-bestand.';
  }
});
