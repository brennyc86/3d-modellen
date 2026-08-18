# AirTag-houder voor een kattentuigje — TPU

Eén stuk, **geen support en nergens een brug**. Voor een B-merk tracker van
**Ø35 × 8 mm**, met aan weerszijden een uitstulping met een gat van **15 × 8 mm**.

![houder](preview_houder.png)

## Hoe het in elkaar zit

Een ronde bak waar de tag van bovenaf onder een rondlopende lip in wordt gedrukt.
Aan weerszijden een platte uitstulping met een **rechtopstaand** gat: je weeft het
tuigje er zelf doorheen en bepaalt zelf of de riem **onder** of **boven** de houder
langs loopt.

![doorsneden](doorsneden.png)

Onder in de bak zit een gat van Ø20 mm om de tag er weer uit te duwen. Loopt de riem
onder de houder door, dan drukt die riem meteen tegen de achterkant van de tag — een
tweede reden waarom hij er niet uit kan.

## Maten

| | mm |
|---|---|
| totaal | 69,2 × 22,0, ronde bak Ø 40,2 |
| hoogte | 12,7 |
| dikte uitstulpingen | 3,0 |
| riemgaten | 15 × 8, hoeken r1,5 |
| tagholte | Ø 35,4 × 8,15 |
| opening onder de lip | Ø 31,0 |
| lip | 2,2 mm overstek |
| gewicht | ~6,4 cm³, geprint ongeveer 5–7 g |

## Wat er is veranderd t.o.v. de eerste versie

Alle drie je punten zaten er inderdaad in:

- **Lip was te mager** — van 1,1 naar **2,2 mm**. In TPU mag dat gerust fors, het
  materiaal rekt gewoon over de tag heen. De hoek is tegelijk flauwer gemaakt
  (39° in plaats van 42° uit het lood), dus de overhang is ook nog eens veiliger.
  ![lipdetail](detail_lip.png)
- **Te slap door de grote openingen** — de veersleuven en de duimuitsparing zijn
  eruit. De wand loopt nu helemaal rond en dicht. In TPU heb je die sleuven niet
  nodig om de tag erin te krijgen, en zonder blijft de bak zijn vorm houden.
- **De tunnel printte niet** — die is weg. De gaten staan nu rechtop door een platte
  uitstulping, dus er wordt **nergens** iets overbrugd. Dat is meteen de reden dat
  je zelf kunt kiezen hoe je de riem laat lopen.

De houder is er ook flink lager door geworden: 12,7 mm in plaats van 20,2 mm.

## Printen (TPU)

De STL staat goed op het bed: **platte onderkant naar beneden, opening omhoog**.

- **TPU 95A**, laag 0,2 mm, **3 wanden**, 25–30 % infill.
- Langzaam: 20–30 mm/s, retractie zo goed als uit, direct drive.
- Support: **uit**. De enige overhang is de lip op 39° en die draagt zichzelf.
- Print op een schoon bed met een dun laagje lijm — TPU hecht anders juist te goed.

Zachter (85A) mag ook; dan wel `LIP` iets kleiner zetten, anders glijdt de tag er bij
een flinke trek doorheen. Wil je hem in PETG in plaats van TPU? Zet dan `LIP` op 1,2 —
2,2 mm krijg je in hard plastic niet meer over de tag heen.

## Als het niet past

Alle maten staan bovenin `airtag_houder.py`. Aanpassen en `python3 airtag_houder.py`
draaien geeft een nieuwe STL.

| Parameter | Wat | Nu |
|---|---|---|
| `TAG_D` / `TAG_H` | maat van je tracker | 35 / 8 |
| `SPEL_D` / `SPEL_H` | speling om de tag | 0,4 / 0,15 |
| `LIP` | hoeveel de lip over de tag valt | 2,2 |
| `LIP_HELLING` | dr/dz van de lip; 1,0 = 45° | 0,8 |
| `GAT_B` / `GAT_L` | riemgat breed × lang | 15 / 8 |
| `UITSTULP_B` / `UITSTULP_D` | uitstulping breed / dik | 22 / 3 |
| `RAND_BIN` / `RAND_BUI` | materiaal binnen / buiten het gat | 2,5 / 4 |
| `DRUK_D` | uitduwgat in de bodem (0 = dicht) | 20 |

**Valt de tag eruit?** `LIP` naar 2,6. **Krijg je hem er niet in?** `LIP` naar 1,8.
**Te lang naar je zin?** `GAT_L` naar 5 maakt hem 6 mm korter; een riempje van 2 mm
dik heeft die 8 mm niet nodig, dat was ruim genomen omdat jij die maat noemde.

## Nog even over de kat

Houder plus tag komt op ongeveer 13 g. Prima voor een volwassen kat. Gebruik het op
een tuigje met veiligheidssluiting en kijk de eerste dagen of er niets schuurt —
TPU is zacht, maar 69 mm is wel een flink stuk op een kattenborst.
