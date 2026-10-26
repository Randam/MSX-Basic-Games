// Basic consent mode: no Google Analytics request until explicit permission.
(() => {
  const measurementId = 'G-0LHYE5QJ2D';
  const key = 'msx-analytics-consent-v1';
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  const production = ['msxbasic.nl', 'www.msxbasic.nl'].includes(location.hostname);
  let choice = null, loaded = false, opener = null;
  try {
    const saved = JSON.parse(localStorage.getItem(key));
    if (saved && Date.now() - saved.updatedAt < lifetime && ['granted', 'denied'].includes(saved.choice)) choice = saved.choice;
  } catch { /* Storage may be unavailable; consent still works for this page. */ }
  const cleanUrl = value => {
    try { const url = new URL(value); return url.origin + url.pathname; } catch { return ''; }
  };
  const banner = document.createElement('aside');
  banner.className = 'analytics-consent';
  banner.setAttribute('role', 'region');
  banner.setAttribute('aria-label', 'Keuze voor bezoekersstatistieken');
  banner.innerHTML = `<div><strong>Mag ik bezoekersstatistieken meten?</strong><p>Met Google Analytics zie ik welke pagina’s en games worden gebruikt. Alleen met jouw toestemming. Weigeren heeft geen invloed op de games. <a href="privacy.html">Meer over privacy &amp; cookies</a>.</p></div><div class="consent-actions"><button type="button" data-choice="denied">Nee, bedankt</button><button type="button" data-choice="granted">Ja, toestaan</button></div>`;
  banner.hidden = choice !== null;
  document.body.append(banner);
  function startAnalytics() {
    if (loaded || choice !== 'granted' || !production) return;
    loaded = true;
    window['ga-disable-' + measurementId] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {analytics_storage:'denied', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('consent', 'update', {analytics_storage:'granted', ad_storage:'denied', ad_user_data:'denied', ad_personalization:'denied'});
    window.gtag('js', new Date());
    window.gtag('config', measurementId, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_expires: 15552000,
      page_location: cleanUrl(location.href),
      page_referrer: cleanUrl(document.referrer)
    });
    const tag = document.createElement('script');
    tag.async = true;
    tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + measurementId;
    tag.dataset.msxAnalytics = 'true';
    document.head.append(tag);
  }
  function removeAnalyticsCookies() {
    for (const cookie of document.cookie.split(';')) {
      const name = cookie.split('=')[0].trim();
      if (!/^_ga(?:_|$)/.test(name)) continue;
      for (const domain of ['', '; domain=' + location.hostname, '; domain=.msxbasic.nl']) {
        document.cookie = name + '=; Max-Age=0; path=/' + domain + '; SameSite=Lax; Secure';
      }
    }
  }
  banner.addEventListener('click', event => {
    const button = event.target.closest('button[data-choice]');
    if (!button) return;
    choice = button.dataset.choice;
    try { localStorage.setItem(key, JSON.stringify({choice, updatedAt:Date.now()})); } catch { /* No persistent storage. */ }
    banner.hidden = true;
    if (choice === 'denied') {
      window['ga-disable-' + measurementId] = true;
      removeAnalyticsCookies();
      // Unload the already-running tag as well, so no cookieless pings continue.
      if (loaded) { location.reload(); return; }
    } else startAnalytics();
    if (opener) opener.focus();
  });
  document.addEventListener('click', event => {
    const button = event.target.closest('[data-cookie-settings]');
    if (!button) return;
    opener = button;
    banner.hidden = false;
    banner.querySelector('button').focus();
  });
  document.addEventListener('msx-game-start', event => {
    if (choice !== 'granted' || !loaded) return;
    window.gtag('event', 'game_start', {game_title:event.detail.game, computer_model:event.detail.computer});
  });
  // Keep a refusal in sync when the visitor changes it in a different tab.
  window.addEventListener('storage', event => {
    if (event.key === key) location.reload();
  });
  startAnalytics();
})();
