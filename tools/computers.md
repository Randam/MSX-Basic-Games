# Computers en compatibiliteit

De eigen SVG-illustraties zijn reproduceerbaar met `python3 tools/draw-computers.py`. Foto’s zijn als referentie bekeken en worden niet meegeleverd.

- Philips VG-8020: zilveren bovenkant, zwarte cartridgeklep, rood modelopschrift en rode cursortoetsen. https://www.msx.org/wiki/Philips_VG-8020
- Philips VG-8235: donkergrijze behuizing, scharnierend toetsenbord, handgreep en diskdrive aan de zijkant. https://www.msx.org/wiki/Philips_VG-8235
- Sony HB-F500P: crèmekleurige systeemkast, dubbele cartridgesleuven en los toetsenbord met numeriek blok. https://www.msx.org/wiki/Category:Sony_HB-F500
- Panasonic FS-A1ST: blauwgrijze kast, lichte toetsen, frontdrive en goudkleurige PCM/statusstrook. https://www.msx.org/wiki/Panasonic_FS-A1ST

WebMSX gebruikt generieke profielen: MSX1E met 64 kB, MSX2E met 256 kB (Philips) of 64 kB (Sony), en MSXTRJ met 256 kB (Panasonic). Deze simuleren de generatie en RAM-grootte, niet alle modelspecifieke ROM’s en geheugenindelingen. De VG-8020 laadt via een virtuele externe diskdrive. De oorspronkelijke gamebestanden zijn ongewijzigd.

## MSX1-controle, 25 oktober 2026

`python3 tools/audit-msx1.py` vereist openMSX 19.1 met de ROM’s voor Philips_VG_8020 en Philips_VY_0010. Gebruik eventueel OPENMSX_BIN voor een ander executable-pad. Per game wordt een geïsoleerde diskmap geladen, bij emulatietijd 3 seconden de datumvraag bevestigd en bij 5 seconden RUN uitgevoerd. Tekst uit VRAM wordt bij 25 en 55 seconden vastgelegd; tussendoor worden N en spatie ingedrukt. Dit is een opstartcontrole, geen volledige speeltest. Resultaat: `tools/compatibility/runtime-msx1.json`.

21 games geven in deze controle geen BASIC-opstartfout. Amazing Joe, The A-Team, Chinese Gup, Magical Ball en Zwemmen gebruiken MSX2-opdrachten (palet, SCREEN 5 of paginabewerkingen). Trons 1 geeft een fout in de originele PLAY-muziekroutine op regel 790. Die fout is afzonderlijk ook op Philips_VG_8235-00 gereproduceerd; het is dus geen MSX1-beperking. Trons 1 blijft beschikbaar bij de andere modellen met toelichting. De MSX1-selectie sluit deze zes games uit.
