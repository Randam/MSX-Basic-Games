# Jer’s MSX

Nederlandstalige speelkamer voor de 27 originele MSX BASIC-games van Jeroen Derwort.

Start vanuit deze map: `python3 -m http.server 4173 --directory dist`. Open http://localhost:4173.

`dist/` is de volledige statische website, zonder installatie of build. Upload die map om zelf te hosten. Games en emulator worden vanaf dezelfde server geladen. Google Fonts zijn optioneel, met lokale fallbacks.

De CSS-computers zijn gestileerd naar Philips VG-8235, Sony HB-F700P en Panasonic FS-A1WSX. Philips en Sony gebruiken het generieke Europese MSX2-profiel; Panasonic het Japanse MSX2+-profiel. Geen modelspecifieke firmware. Games zijn ongewijzigd, inclusief de oorspronkelijke Fantasieland 3 ZIP.

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

De achtergrondpagina behandelt ook de MSX-standaard: de gezamenlijke basis van verschillende merken, de introductiejaren en verschillen van MSX1/MSX2/MSX2+/turbo R, softwarecompatibiliteit en de drie modellen in de speelkamer. Bronnen zijn bij de tekst en vergelijkingstabel gelinkt (MSX Wiki, MSX FAQ en MRC).
