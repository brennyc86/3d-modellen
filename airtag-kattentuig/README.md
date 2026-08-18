# AirTag-houder voor een kattentuigje — TPU

Eén stuk, **geen support en nergens een brug**. Voor een B-merk tracker van
**Ø35 × 8 mm**, met aan weerszijden een uitstulping met een gat van **15 × 8 mm**
(8 mm zodat ook de sluitclip van het tuigje erdoorheen kan).

![houder](preview_houder.png)

## Hoe het in elkaar zit

Een ronde bak waar de tag van bovenaf onder een rondlopende lip in wordt gedrukt.
Aan weerszijden een platte uitstulping met een **rechtopstaand** gat: je weeft het
tuigje er zelf doorheen en bepaalt zelf of de riem **onder** of **boven** de houder
langs loopt.

Onder in de bak zit een gat van Ø20 mm om de tag er weer uit te duwen. Loopt de riem
onder de houder door, dan drukt die riem meteen tegen de achterkant van de tag.

![doorsneden](doorsneden.png)

## Alle randen afgerond (v5 — zo rond als printbaar is)

Er zit geen scherpe kant meer aan, binnen noch buiten:

| Rand | v4 | nu |
|---|---|---|
| bovenrand van de bak, buitenkant | r1,8 | **r3,2** — de bovenrand is nu een volle rol |
| onderkant van de lip (langs de tag) | r1,0 | **r1,8** |
| binnenrand bovenaan (de liptip) | r0,6 | **r1,0** |
| binnenhoek onderin de tagholte | r0,5 | **r0,8** |
| randen uitstulpingen + rond de riemgaten | r1,0 | **r1,5** |
| bedzijde (kant van de kat) | 45° afschuining | **gebogen aanloop, r1,8** |

De bovenrand van de bak is met r3,2 op de wanddikte na volledig rondgezet: van de
buitenwand loopt hij in één bocht over de top naar de lip, met nog maar 0,4 mm vlak
op de kruin. De lip loopt als één doorlopende bocht om de tag heen.

**De bedzijde is niet langer een vlakke afschuining.** Een echte afronding op laag 1
begint met een flinterdunne rand die omkrult, dus dat kan niet. In plaats daarvan
start de rand nu met een recht stukje van precies 45° en buigt daarna met r1,8 de
wand in — het rondste wat op de eerste laag mogelijk is, en in de hand niet van een
afronding te onderscheiden.

Kosten: 0,8 mm hoger (14,7 in plaats van 13,9 mm) en de uitstulpingen zijn van 3,2
naar 3,8 mm gegaan, zodat er tussen de afronding boven en de aanloop onder nog
recht materiaal overblijft.

## Overhang: gecontroleerd, geen support

`airtag_houder.py` meet zelf na hoeveel neerwaarts vlak er steiler dan 45° staat:

```
overhangcontrole: 0.00 mm2 van 852 mm2 neerwaarts vlak staat steiler dan 45°
                  -> GEEN support nodig
```

Ondanks alle extra rondingen staat er nu geen enkel vlak boven de 45°. De lip zelf
staat op 39° uit het lood.

![lipdetail](detail_lip.png)

## Maten

| | mm |
|---|---|
| totaal | 69,2 × 22,0, ronde bak Ø 40,2 |
| hoogte | 14,68 |
| dikte uitstulpingen | 3,8 |
| riemgaten | 15 × 8, hoeken r1,5 |
| tagholte | Ø 35,4 × 8,15 |
| nauwste opening onder de lip | Ø 31,0 |
| lip | 2,2 mm overstek onder 39° |
| gewicht | ~7,1 cm³, geprint ongeveer 5–7 g |

## Printen (TPU)

De STL staat goed op het bed: **platte onderkant naar beneden, opening omhoog**.

- **TPU 95A**, laag 0,2 mm, **3 wanden**, 25–30 % infill.
- Langzaam: 20–30 mm/s, retractie zo goed als uit, direct drive.
- Support: **uit**.
- Print op een schoon bed met een dun laagje lijm — TPU hecht anders juist te goed.

## Als het niet past

Alle maten staan bovenin `airtag_houder.py`. Aanpassen en `python3 airtag_houder.py`
draaien geeft een nieuwe STL.

| Parameter | Wat | Nu |
|---|---|---|
| `TAG_D` / `TAG_H` | maat van je tracker | 35 / 8 |
| `SPEL_D` / `SPEL_H` | speling om de tag | 0,4 / 0,15 |
| `LIP` | hoeveel de lip over de tag valt | 2,2 |
| `LIP_HELLING` | dr/dz van de lip; 1,0 = 45° | 0,8 |
| `ROND_RAND` … `ROND_TAB` | de afrondingen, per rand | 3,2 … 1,5 |
| `AFSCH_ONDER` / `ROND_ONDER` | aanloop aan de bedzijde: inzet op laag 1 / radius | 0,9 / 1,8 |
| `GAT_B` / `GAT_L` | riemgat breed × lang | 15 / 8 |
| `UITSTULP_B` / `UITSTULP_D` | uitstulping breed / dik | 22 / 3,8 |
| `DRUK_D` | uitduwgat in de bodem (0 = dicht) | 20 |

**Nog steeds te hard aan een rand?** Zet de betreffende `ROND_*` hoger; de
overhangcontrole onderaan de uitvoer waarschuwt vanzelf als het te ver gaat.
**Valt de tag eruit?** `LIP` naar 2,6. **Te stug erin?** `LIP` naar 1,8.

## Opnieuw genereren

```bash
pip install --break-system-packages numpy shapely trimesh manifold3d mapbox_earcut matplotlib
python3 airtag_houder.py     # schrijft airtag_houder.stl
python3 render.py            # previews + doorsneden
```
