# Jer’s MSX

Nederlandstalige speelkamer voor de 27 originele MSX BASIC-games van Jeroen Derwort.

Start vanuit deze map: `python3 -m http.server 4173 --directory dist`. Open http://localhost:4173.

`dist/` is de volledige statische website, zonder installatie of build. Upload die map om zelf te hosten. Games en emulator worden vanaf dezelfde server geladen. Google Fonts zijn optioneel, met lokale fallbacks.

De eigen SVG-illustraties volgen de Philips VG-8020, Philips VG-8235, Sony HB-F700P en Panasonic FS-A1ST. WebMSX gebruikt generieke MSX1-, MSX2- en turbo R-profielen met passende RAM-instellingen; geen modelspecifieke firmware. De VG-8020-selectie bevat 21 opstartgeteste games. Zie `tools/computers.md` voor fotoreferenties en de compatibiliteitscontrole. Games zijn ongewijzigd, inclusief de oorspronkelijke Fantasieland 3 ZIP.

Games en screenshots: https://www.jeroenderwort.nl/wp-content/uploads/jermsx/jermsx.html

Emulator: WebMSX 6.0 embedded-release uit https://github.com/ppeccin/WebMSX. Copyright Paulo Augusto Peccin; zie de verklaring in dist/emulator/wmsx.js en https://webmsx.org. Model- en merknamen behoren aan hun eigenaren.

MSX-logo: de originele vectorvorm via https://commons.wikimedia.org/wiki/File:MSX-Logo.svg (PD-textlogo; merkrechten blijven van toepassing). Lokaal opgeslagen in dist/assets/msx-logo.svg.

## GitHub Pages

Productiedomein: https://msxbasic.nl. Een push naar `main` publiceert automatisch `dist/` via `.github/workflows/pages.yml`. GitHub Pages is ingesteld op GitHub Actions. `www.msxbasic.nl` verwijst naar het hoofddomein.

Cloudflare DNS: vier DNS-only A-records voor `@` naar `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; een DNS-only CNAME `www` naar `randam.github.io`.

## Over MSX-BASIC

`dist/msx-basic.html` bevat de achtergrondpagina, een klikbare screenshotgalerij, een opdrachtenoverzicht en een uitvoerbare beginnerslisting (`dist/examples/HALLO.BAS`). De nieuwe voorbeeldcode is apart herkenbaar van Jeroens historische programma’s.

Teksten en originele media zijn gebaseerd op Jeroen Derworts artikelen:
- https://www.jeroenderwort.nl/msx-basic-kracht/ (14 april 2019): listing, BOSS, sprite-editor, FM-PAC Basic Tracker en hiërogliefenvertaler.
- https://www.jeroenderwort.nl/msx-tijdschriften/ (12 september 2025): foto van de MSX-tijdschriften.

De media staan lokaal in `dist/assets/learn/`; de pagina verwijst bij de inhoud terug naar de oorspronkelijke artikelen. Externe naslagbronnen: MSX Wiki, het MCM/MCCM-archief, het MRC-forum en de officiële WebMSX-repository. Links en documentatie gecontroleerd op 24 oktober 2026.

De achtergrondpagina behandelt ook de MSX-standaard: de gezamenlijke basis van verschillende merken, de introductiejaren en verschillen van MSX1/MSX2/MSX2+/turbo R, softwarecompatibiliteit en de vier modellen in de speelkamer. Bronnen zijn bij de tekst en vergelijkingstabel gelinkt (MSX Wiki, MSX FAQ en MRC).

## HTTPS en social previews

GitHub Pages verzorgt het TLS-certificaat voor `msxbasic.nl` en `www.msxbasic.nl`; HTTPS wordt afgedwongen. Beide pagina’s hebben hun eigen canonical URL, Open Graph-titel en beschrijving, plus Twitter/X `summary_large_image`-metadata. De gedeelde afbeelding is `dist/assets/social-msxbasic.jpg` (1200 × 630). Deze gebruikt het bestaande logo, de VG-8235-illustratie en het originele Airplane-screenshot. De reproduceerbare compositie staat in `tools/social-card.html`: serveer de projectmap en maak een screenshot van die pagina met een viewport van exact 1200 × 630 pixels. Alleen `dist/` wordt gepubliceerd.

## MSX-verzameling

`dist/verzameling.html` presenteert alle 39 modellen van https://www.jeroenderwort.nl/msx-computer-verzameling/ (overgenomen op 25 oktober 2026), met 15 merken, persoonlijke beschrijvingen en aanpassingen. Foto’s tonen modellen, niet noodzakelijk Jeroens eigen machines. De volledige inhoud staat statisch in de HTML; `collection.js` voegt zoeken op alle tekst en gecombineerde merk- en generatiefilters toe. Filteren op generatie volgt de huidige configuratie: de omgebouwde HX-10 valt onder MSX2+, de OneChipBook apart onder Compatible.

Brongegevens: `dist/collection.json`. Na inhoudswijzigingen: `python3 tools/build-collection.py`. Dit maakt alleen `verzameling.html` opnieuw. De bronfoto’s staan lokaal in `dist/assets/collection/`; zeven kleine of minder geschikte afbeeldingen zijn vervangen door MSX Wiki-foto’s (Hitachi MB-H3, NMS 801, FS-A1WSX, FS-A1ST, PHC-77, PHC-70FD en HX-20). Herkomst en fotolinks staan per model in JSON en bij de details op de pagina. De foto’s blijven volledig zichtbaar via object-fit: contain. De paginastijl staat in `collection.css`.

Kleine redactionele correcties ten opzichte van de bron: Mitsubishi als merk bij ML-TS2, officieel modelnummer HB-F700P, correcte verwijzingen voor HB-F5/HB-F700P/HX-20, 4 MB bij de omgebouwde HX-10 en 512 kB als uitbreiding bij FS-A1ST. Turbo R is omschreven als de laatste officiële generatie; de FS-A1GT volgde nog op de FS-A1ST. De speelkamer gebruikt eveneens de HB-F700P met 256 kB RAM.

Aanvulling 25 oktober 2026: Sony XV-J777 toegevoegd als MSX2-gebaseerde videotitler, met bron en modelfoto uit de MSX Wiki. Het introductiejaar is daar onbekend en blijft als onbekend vermeld. De Canon is door Jeroen verduidelijkt als V-20 en toegevoegd met gegevens van de Europese uitvoering uit 1985. De collectie telt nu 41 modellen van 16 merken. De paginagenerator synchroniseert nu ook de tekstuele totalen op de homepage, in metadata en in de social-compositie; de JPEG moet na een wijziging opnieuw worden vastgelegd.

## Google Analytics 4

Ingericht op 26 oktober 2026 onder Derwort Media (account 1166867): property **MSX BASIC — msxbasic.nl** (560804087), webstream **MSX BASIC website** (16207383940), metings-ID **G-0LHYE5QJ2D**. Tijdzone Nederland, valuta EUR, branche Games. Bewaring van gebruikers- en gebeurtenisgegevens: twee maanden, reset bij nieuwe activiteit uit. Er zijn geen advertentiekoppelingen toegevoegd. Verbeterde meting: paginaweergaven, scrollen, uitgaande klikken en bestanddownloads; sitezoeken, formulierinteracties en video-engagement uit.

`dist/analytics.js` implementeert basic consent mode: de Google-tag wordt alleen na expliciete toestemming geladen, uitsluitend op msxbasic.nl / www.msxbasic.nl. Ads-opslag, advertentiepersonalisatie en Google Signals blijven uit. Keuze en cookies verlopen na 180 dagen (cookieperiode kan worden vernieuwd). Query en hash worden uit de ingestelde pagina- en verwijzeradressen verwijderd. `game_start` bevat `game_title` en `computer_model`; die zijn als gebeurtenisdimensies Game en Computermodel geregistreerd in GA4. Bij intrekken worden de Analytics-cookies verwijderd, verdere meting geblokkeerd en de pagina herladen. Footerbediening staat op alle inhoudspagina’s; uitleg staat in `privacy.html`. De emulatorpagina is bewust niet apart getagd, om dubbele paginaweergaven te vermijden.

Controleer met `node --test tools/test-analytics.mjs`. Google-documentatie: https://developers.google.com/tag-platform/security/concepts/consent-mode en https://developers.google.com/tag-platform/security/guides/consent . Het account bestond al en de voorwaarden waren al geaccepteerd; er zijn geen nieuwe voorwaarden namens de gebruiker geaccepteerd.
