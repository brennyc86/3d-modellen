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

## Alle randen afgerond (v4)

Alles wat de kat of de tag kan raken is nu rond in plaats van scherp:

| Rand | Behandeling |
|---|---|
| bovenrand van de bak, buitenkant | volledig rondgezet, r1,8 |
| onderkant van de lip (langs de tag) | r1,0 — vloeit in de wand van de tagholte |
| binnenrand bovenaan (de liptip) | r0,6 |
| binnenhoek onderin de tagholte | r0,5 |
| randen van de uitstulpingen + rond de riemgaten | r1,0 |
| alles aan de bedzijde (kant van de kat) | 45° × 0,9 afschuining |

De lip loopt daardoor als één vloeiende bocht om de tag heen in plaats van als een
harde ring. Omdat de tag zelf ook rond is, nestelt zijn bovenrand in de onderste
afronding — dat pakt tegelijk een fractie steviger.

**Waarom de bedzijde een afschuining is en geen afronding:** een afronding op laag 1
begint met een flinterdunne rand die omkrult. Een afschuining van 45° start met
volle breedte en voelt in TPU praktisch net zo zacht.

De houder is er 1,2 mm hoger door geworden (13,9 in plaats van 12,7 mm) en de
uitstulpingen zijn van 3,0 naar 3,2 mm gegaan, zodat er onder de afrondingen genoeg
vlees overblijft.

## Overhang: gecontroleerd, geen support

`airtag_houder.py` meet zelf na hoeveel neerwaarts vlak er steiler dan 45° staat:

```
overhangcontrole: 0.15 mm2 van 426 mm2 neerwaarts vlak staat steiler dan 45°
                  -> GEEN support nodig
```

Die 0,15 mm² zijn een paar splinters op de overgang van de afschuining; verder staat
er niets boven de 45°. De lip zelf staat op 39° uit het lood.

![lipdetail](detail_lip.png)

## Maten

| | mm |
|---|---|
| totaal | 69,2 × 22,0, ronde bak Ø 40,2 |
| hoogte | 13,86 |
| dikte uitstulpingen | 3,2 |
| riemgaten | 15 × 8, hoeken r1,5 |
| tagholte | Ø 35,4 × 8,15 |
| nauwste opening onder de lip | Ø 31,0 |
| lip | 2,2 mm overstek onder 39° |
| gewicht | ~6,8 cm³, geprint ongeveer 5–7 g |

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
| `ROND_RAND` … `ROND_TAB` | de afrondingen, per rand | 1,8 … 1,0 |
| `AFSCH_ONDER` | afschuining aan de bedzijde | 0,9 |
| `GAT_B` / `GAT_L` | riemgat breed × lang | 15 / 8 |
| `UITSTULP_B` / `UITSTULP_D` | uitstulping breed / dik | 22 / 3,2 |
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
