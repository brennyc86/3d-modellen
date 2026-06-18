# 3D-modellen

Algemene verzameling 3D-printbare modellen die Claude voor Brendan ontwerpt.
Elk project is parametrisch (Python: `shapely` + `trimesh` + `manifold3d`) met
kant-en-klare STL's, previews en een eigen README.

## Projecten

| Map | Wat | Status |
|---|---|---|
| [`afdekplaat-scheepsopening`](afdekplaat-scheepsopening/) | 2-delig afdekplaatje voor een handgezaagde opening in het schot (kat weg bij de elektrakabels). Insteekrichel met vol contact, lap-naad + 2 schroeven, open kabelsleuf. Past op Bambu A1 (≤243 mm). | ✅ v4 |
| [`a1mini-boot-montage`](a1mini-boot-montage/) | Pootklemmen om een Bambu Lab A1 mini vast te zetten op een (te krap) plankje op de zeilboot. Schroeven binnen de footprint. | ✅ v1 |

## Zelf opnieuw genereren

```bash
pip install --break-system-packages numpy shapely trimesh manifold3d matplotlib
cd <project>
python3 <script>.py        # schrijft de STL('s)
python3 render.py          # optioneel: previews
```

> Alle maten staan bovenin het Python-bestand van elk project en zijn bedoeld om na
> opmeten aan te passen — daarna één keer opnieuw draaien voor nieuwe STL's.
