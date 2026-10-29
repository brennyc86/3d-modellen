# Kangoo-haakje (sierverlichting)

Haakje voor lichtsnoeren dat je **direct in de schroefdraadgaten** (vliegtuigboxen) van de
Renault Kangoo draait. Alleen voor lichte belasting; trekkracht schuin op de stift breekt hem.
De draadmaat van de gaten is niet bevestigd, dus er is een set. Probeer welke bout soepel
indraait en print die maat.

## Haakje met eigen draad (hoofdversie)

| Bestand | Draad | Spoed | Stiftlengte |
|---|---|---|---|
| `kangoo_haakje_draad_M3.stl` | M3 | 0,5 | 12 mm |
| `kangoo_haakje_draad_M4.stl` | M4 | 0,7 | 12 mm |
| `kangoo_haakje_draad_M5.stl` | M5 | 0,8 | 12 mm |
| `kangoo_haakje_draad_M6.stl` | M6 | 1,0 | 12 mm |
| `kangoo_haakje_draad_M8.stl` | M8 | 1,25 | 12 mm |

- ISO-grof draad, rechtsdraaiend, stift 0,25 mm onder nominaal (printspeling). Zit hij te los
  of te strak: `SPELING` in `gen_draad.py` aanpassen (±0,1) en opnieuw draaien.
- **Printen:** haakje plat op het bed, stift omhoog, geen support. PETG/ASA (PLA wordt zacht in
  een warme auto). 4 wanden, 40% infill; kleine draad (M3/M4) print grof, een 0,2 mm laag helpt.
- Draai alleen handvast aan. Een geprint draad schuift niet op moment dat het strak staat, en breekt dan.

## Haakje met losse bout (alternatief)

`kangoo_haakje_M5/M6/M8/M10.stl`: gat voor een bout met cilinderkop door het midden. Veel
sterker, maar je hebt een bout nodig (`gen.py`).

Maten aanpassen: bovenin het script, daarna `python3 gen_draad.py` / `python3 gen.py`.
