#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AirTag-houder voor een kattentuigje -- EEN STUK, TPU, geen support
==================================================================
Voor een B-merk tracker van Ø35 x 8 mm.

Een ronde bak met aan weerszijden een platte uitstulping met een gat van 15 x 8 mm.
Het gat staat RECHTOP (van boven naar onder door de lip heen), dus er wordt nergens
iets overbrugd -- geen tunnel, geen brug, niets wat TPU niet aankan. Je weeft het
tuigje er zelf doorheen en kiest zelf of de riem onder of boven de houder langs loopt.

De tag klikt van bovenaf onder een rondlopende lip van 2,2 mm. De wand is verder
helemaal dicht: geen veersleuven, want in TPU wordt het geheel daar te slap van.
De rek van het materiaal is genoeg om de tag erin te drukken. Eruit duw je hem
door het gat in de bodem.

Print-orientatie zit al in de STL: platte onderkant op het bed, opening omhoog.
Enige overhang is de lip, en die staat op 39 graden uit het lood.

Maten in mm. Z=0 = kant tegen de kat, Z omhoog = van de kat af.
"""
import numpy as np
import trimesh
from shapely.geometry import box as sbox, Point

ENGINE = "manifold"

# ============================================================
#  PARAMETERS  -- meet je eigen tag/riem na!
# ============================================================
TAG_D      = 35.0   # diameter van de tag (METEN)
TAG_H      = 8.0    # dikte van de tag (METEN)
SPEL_D     = 0.4    # speling op de diameter (TPU: krap mag, het rekt)
SPEL_H     = 0.15   # speling op de dikte

WAND       = 2.4    # wanddikte van de bak
BODEM      = 1.8    # dikte van de bodem

LIP        = 2.2    # hoeveel de lip over de tag valt. TPU rekt, dus dit mag fors
LIP_HELLING = 0.8   # dr/dz van de lip; 1.0 = 45 gr. 0.8 = 39 gr = veilig voor TPU

UITSTULP_B = 22.0   # breedte van de uitstulpingen
UITSTULP_D = 3.0    # dikte van de uitstulpingen
GAT_B      = 15.0   # gat: breedte (dwars op de riem)
GAT_L      = 8.0    # gat: lengte (in de looprichting van de riem)
GAT_R      = 1.5    # afronding hoeken van het gat
RAND_BIN   = 2.5    # materiaal tussen de bak en het gat
RAND_BUI   = 4.0    # materiaal tussen het gat en het uiteinde
EIND_R     = 5.0    # afronding van de hoeken van de uitstulping
FILET      = 3.0    # afronding waar de uitstulping in de bak overgaat

DRUK_D     = 20.0   # gat in de bodem om de tag eruit te duwen (0 = dicht)
RAND_AFSCH = 0.6    # afschuining buitenste bovenrand
ONDER_AFSCH = 0.8   # afschuining onderrand, kant van de kat

QS = 128            # segmenten in de ronde delen

# ============================================================
#  AFGELEIDE MATEN
# ============================================================
R_HOLTE = TAG_D/2 + SPEL_D/2           # 17.70  binnenmaat tagholte
R_BUI   = R_HOLTE + WAND               # 20.10  buitenradius van de bak
R_LIP   = R_HOLTE - LIP                # 15.50  vrije opening (straal)

z_lip0  = BODEM + TAG_H + SPEL_H       # 9.95   hier begint de lip
z_top   = z_lip0 + LIP/LIP_HELLING     # 12.70  bovenrand

GAT_X0  = R_BUI + RAND_BIN             # 22.60  binnenkant gat
GAT_X1  = GAT_X0 + GAT_L               # 30.60  buitenkant gat
TOT_L   = 2*(GAT_X1 + RAND_BUI)        # 69.20  totale lengte


# ============================================================
#  HULPJES
# ============================================================
def U(ms):   return trimesh.boolean.union(ms, engine=ENGINE)
def D(a, b): return trimesh.boolean.difference([a, b], engine=ENGINE)


def wentel(profiel):
    """Gesloten 2D-profiel (r, z) rondwentelen om de Z-as."""
    p = np.asarray(profiel, dtype=float)
    if not np.allclose(p[0], p[-1]):
        p = np.vstack([p, p[0]])
    m = trimesh.creation.revolve(p, sections=QS)
    m.merge_vertices()
    if m.volume < 0:
        m.invert()
    return m


def uitpers(poly, za, zb):
    m = trimesh.creation.extrude_polygon(poly, height=zb-za)
    m.apply_translation([0, 0, za])
    return m


def cyl(r, za, zb, x=0.0, y=0.0):
    c = trimesh.creation.cylinder(radius=r, height=zb-za, sections=QS)
    c.apply_translation([x, y, (za+zb)/2])
    return c


# ============================================================
#  HET MODEL
# ============================================================
def plattegrond():
    """Bovenaanzicht: ronde bak + twee uitstulpingen, met filet in de overgang."""
    vorm = Point(0, 0).buffer(R_BUI, resolution=QS//4)
    for teken in (1, -1):
        eind = teken * (GAT_X1 + RAND_BUI)
        lip = sbox(min(0, eind), -UITSTULP_B/2, max(0, eind), UITSTULP_B/2)
        lip = lip.buffer(-EIND_R).buffer(EIND_R, join_style=1)   # hoeken rond
        vorm = vorm.union(lip)
    # sluiting: vult de holle hoeken bij de overgang bak <-> uitstulping
    return vorm.buffer(FILET, join_style=1).buffer(-FILET, join_style=1)


def maak_houder():
    plan = plattegrond()

    # --- onderste laag: bodem + de twee uitstulpingen
    onder = uitpers(plan, 0.0, UITSTULP_D)
    # gebroken onderrand (kant van de kat)
    trap = [uitpers(plan.buffer(-ONDER_AFSCH*(4-i)/4), i*ONDER_AFSCH/4,
                    (i+1)*ONDER_AFSCH/4 + 0.01) for i in range(4)]
    onder = U([uitpers(plan, ONDER_AFSCH, UITSTULP_D)] + trap)

    # --- de ronde bak erbovenop
    bak = wentel([
        (0.0,   0.0),
        (R_BUI, 0.0),
        (R_BUI, z_top - RAND_AFSCH),
        (R_BUI - RAND_AFSCH, z_top),      # gebroken buitenrand, 45 gr = printbaar
        (0.0,   z_top),
    ])
    romp = U([onder, bak])

    # --- tagholte met de lip erboven
    holte = wentel([
        (0.0,     BODEM),
        (R_HOLTE, BODEM),
        (R_HOLTE, z_lip0),
        (R_LIP,   z_top),                 # de lip: 39 gr. uit het lood
        (0.0,     z_top + 1.0),
        (0.0,     BODEM),
    ])
    romp = D(romp, holte)

    # --- gat in de bodem om de tag eruit te duwen
    if DRUK_D > 0:
        romp = D(romp, cyl(DRUK_D/2, -1.0, BODEM + 0.01))

    # --- de twee riemgaten: rechtop, dus geen brug, geen support
    gaten = []
    for teken in (1, -1):
        g = sbox(GAT_X0, -GAT_B/2, GAT_X1, GAT_B/2) \
                .buffer(-GAT_R).buffer(GAT_R, join_style=1)
        if teken < 0:
            g = sbox(-GAT_X1, -GAT_B/2, -GAT_X0, GAT_B/2) \
                    .buffer(-GAT_R).buffer(GAT_R, join_style=1)
        gaten.append(uitpers(g, -1.0, UITSTULP_D + 1.0))
    romp = D(romp, U(gaten))

    return romp


def tag_dummy():
    return cyl(TAG_D/2, BODEM, BODEM + TAG_H)


if __name__ == "__main__":
    m = maak_houder()
    m.export("airtag_houder.stl")
    print(f"HOUDER: dicht={m.is_watertight} delen={m.body_count} "
          f"bbox={np.round(m.extents, 2)} volume={m.volume/1000:.2f} cm3 "
          f"(~{m.volume*1.21/1000:.1f} g TPU massief)")
    print(f"  {TOT_L:.1f} x {UITSTULP_B:.1f} mm uitstulpingen, bak Ø{2*R_BUI:.1f}, "
          f"hoogte {z_top:.2f} mm")
    print(f"  tagholte Ø{2*R_HOLTE:.1f} x {TAG_H+SPEL_H:.2f}  |  opening Ø{2*R_LIP:.1f} "
          f"|  lip {LIP:.1f} mm, overstek "
          f"{np.degrees(np.arctan(LIP_HELLING)):.0f}° uit het lood")
    print(f"  riemgaten {GAT_L:.0f} x {GAT_B:.0f} mm, rechtop door de uitstulping "
          f"(dikte {UITSTULP_D:.1f} mm)")
