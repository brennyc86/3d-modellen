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

## De bedzijde (v6) — de kant die tegen de kat aan komt

| Rand | v5 | nu |
|---|---|---|
| **bedzijde: inzet op laag 1** | 0,9 | **1,6** |
| **bedzijde: radius van de aanloop** | r1,8 | **r3,2** |
| bedzijde: over welke hoogte hij wegrolt | 1,65 mm | **2,93 mm** |
| rand van het uitduwgat | 45° × 1,2 | **aanloop 1,0 / r2,0** |
| bovenrand van de bak, buitenkant | r3,2 | r3,2 |
| onderkant van de lip (langs de tag) | r1,8 | r1,8 |
| binnenrand bovenaan (de liptip) | r1,0 | r1,0 |
| binnenhoek onderin de tagholte | r0,8 | r0,8 |
| bovenrand van de uitstulpingen | r1,5 | r1,4 |

**Wat er niet kan:** een echte afronding aan de bedzijde. Laag 1 zou daar als een
flintertje beginnen en omkrullen — dat wordt geen ronding maar een rafel.

**Wat wel kan, en nu ruim twee keer zo ver gaat:** de rand begint op laag 1 met een
recht stuk van precies 45° en buigt daarna met r3,2 de wand in. De omtrek ligt op
laag 1 nu **1,6 mm** naar binnen en rolt over bijna **3 mm hoogte** naar de volle
maat. De kat voelt daardoor geen plaatrand meer maar een schouder die wegloopt.

Het uitduwgat in de bodem ligt ook tegen de kat aan en heeft dezelfde behandeling
gekregen: die rand loopt nu vloeiend de bodem in in plaats van met een 45° kantje.

Het contactvlak blijft met ~9,7 cm² ruim genoeg om de druk te spreiden.

**De riemgaten krijgen expres een kleinere aanloop** (1,0 / r1,2). Die raken de kat
niet, en met de grote aanloop van de omtrek zou er tussen gat en rand van de
uitstulping te weinig materiaal overblijven. Nu is dat op laag 1 nog 1,3 mm, en
daarboven meteen ruim 3 mm.

Kosten: de uitstulpingen zijn van 3,8 naar 4,4 mm gegaan, want de aanloop van 2,93 mm
plus de afronding van 1,4 mm bovenop moet er wel in passen. De houder blijft
14,7 mm hoog.

## Overhang: gecontroleerd, geen support

`airtag_houder.py` meet zelf na hoeveel neerwaarts vlak er steiler dan 45° staat:

```
overhangcontrole: 0.12 mm2 van 1180 mm2 neerwaarts vlak staat steiler dan 46°
                  -> GEEN support nodig
```

De grens staat op 46° en niet op 45°, omdat de aanloop aan de bedzijde met opzet
precies 45° is — door afrondingsruis vallen die facetten anders willekeurig net aan
de verkeerde kant van de grens. Wat er overblijft is 0,12 mm² aan splinters op de
overgangen. De lip zelf staat op 39° uit het lood.

![lipdetail](detail_lip.png)

## Maten

| | mm |
|---|---|
| totaal | 69,2 × 22,0, ronde bak Ø 40,2 |
| hoogte | 14,68 |
| dikte uitstulpingen | 4,4 |
| riemgaten | 15 × 8, hoeken r1,5 |
| tagholte | Ø 35,4 × 8,15 |
| nauwste opening onder de lip | Ø 31,0 |
| lip | 2,2 mm overstek onder 39° |
| gewicht | ~7,2 cm³, geprint ongeveer 5–7 g |

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
| `ROND_RAND` … `ROND_TAB` | de afrondingen, per rand | 3,2 … 1,4 |
| `AFSCH_ONDER` / `ROND_ONDER` | **aanloop bedzijde**: inzet op laag 1 / radius | 1,6 / 3,2 |
| `AFSCH_GAT` / `ROND_GAT` | idem voor de riemgaten | 0,6 / 1,2 |
| `AFSCH_DRUK` / `ROND_DRUK` | idem voor het uitduwgat | 1,0 / 2,0 |
| `GAT_B` / `GAT_L` | riemgat breed × lang | 15 / 8 |
| `UITSTULP_B` / `UITSTULP_D` | uitstulping breed / dik | 22 / 4,4 |
| `DRUK_D` | uitduwgat in de bodem (0 = dicht) | 20 |

**Nog steeds te hard aan de bedzijde?** Zet `AFSCH_ONDER` en `ROND_ONDER` hoger —
dat is de enige knop die daar echt helpt. Let dan wel op twee dingen: `UITSTULP_D`
moet minstens de aanlooplengte + `ROND_TAB` zijn, en het materiaal tussen gat en
rand van de uitstulping wordt kleiner (`UITSTULP_B` mee omhoog of `AFSCH_GAT`
omlaag). Het script gooit een duidelijke fout als het echt niet meer past.
**Valt de tag eruit?** `LIP` naar 2,6. **Te stug erin?** `LIP` naar 1,8.

## Opnieuw genereren

```bash
pip install --break-system-packages numpy shapely trimesh manifold3d mapbox_earcut matplotlib
python3 airtag_houder.py     # schrijft airtag_houder.stl
python3 render.py            # previews + doorsneden
```
