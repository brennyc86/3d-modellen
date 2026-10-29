# Kangoo-haakje (sierverlichting)

Haakje voor lichtsnoeren met een **gladde pen met een kleine ribbel**, die je in de
schroefdraadgaten (vliegtuigboxen) van de Renault Kangoo duwt. Er komt geen draad aan het
haakje, dus de draad in de auto blijft heel voor de echte koffers. Alleen voor lichte
belasting (sierverlichting). De draadmaat van de gaten is niet bevestigd, dus er is een set.

| Bestand | Voor draad | Pen ⌀ | Ribbel ⌀ | Penlengte |
|---|---|---|---|---|
| `kangoo_haakje_pen_M3.stl` | M3 | 2,26 | 2,73 | 12 mm |
| `kangoo_haakje_pen_M4.stl` | M4 | 3,04 | 3,62 | 12 mm |
| `kangoo_haakje_pen_M5.stl` | M5 | 3,93 | 4,57 | 12 mm |
| `kangoo_haakje_pen_M6.stl` | M6 | 4,72 | 5,46 | 12 mm |
| `kangoo_haakje_pen_M8.stl` | M8 | 6,45 | 7,32 | 12 mm |

- Pen = kerndiameter van het draad min 0,2 mm; de ribbel steekt ~0,3–0,45 mm uit en haakt in de
  draadgroef. Een gleuf (9 mm diep) in het uiteinde laat de pen meeveren bij het indrukken.
- Zit hij te los: `RIBBEL` omhoog in `gen_pen.py` (0,5 → 0,65). Te strak: omlaag of `SPELING` omhoog.
- **Printen:** haakje plat op het bed, pen omhoog, geen support (ribbel heeft 45°-flanken). PETG
  (iets buigzaam, breekt minder dan PLA/ASA), 4 wanden, 100% infill in de pen als dat kan.
- Indrukken met een lichte draaibeweging; eruit trekken kan zonder gereedschap.

## Alternatief: losse bout

`kangoo_haakje_M5/M6/M8/M10.stl`: gat voor een bout met cilinderkop door het midden (`gen.py`).
Veel sterker, maar vergt een bout.

Maten aanpassen: bovenin het script, daarna `python3 gen_pen.py` / `python3 gen.py`.
