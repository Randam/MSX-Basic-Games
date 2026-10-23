# Jer’s MSX

Nederlandstalige speelkamer voor de 27 originele MSX BASIC-games van Jeroen Derwort.

Start vanuit deze map: `python3 -m http.server 4173 --directory dist`. Open http://localhost:4173.

`dist/` is de volledige statische website, zonder installatie of build. Upload die map om zelf te hosten. Games en emulator worden vanaf dezelfde server geladen. Google Fonts zijn optioneel, met lokale fallbacks.

De CSS-computers zijn gestileerd naar Philips VG-8235, Sony HB-F700P en Panasonic FS-A1WSX. Philips en Sony gebruiken het generieke Europese MSX2-profiel; Panasonic het Japanse MSX2+-profiel. Geen modelspecifieke firmware. Games zijn ongewijzigd, inclusief de oorspronkelijke Fantasieland 3 ZIP.

Games en screenshots: https://www.jeroenderwort.nl/wp-content/uploads/jermsx/jermsx.html

Emulator: WebMSX 6.0 embedded-release uit https://github.com/ppeccin/WebMSX. Copyright Paulo Augusto Peccin; zie de verklaring in dist/emulator/wmsx.js en https://webmsx.org. Model- en merknamen behoren aan hun eigenaren.

MSX-logo: de originele vectorvorm via https://commons.wikimedia.org/wiki/File:MSX-Logo.svg (PD-textlogo; merkrechten blijven van toepassing). Lokaal opgeslagen in dist/assets/msx-logo.svg.
