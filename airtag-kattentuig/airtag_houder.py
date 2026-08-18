#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AirTag-houder voor een kattentuigje -- EEN STUK, geen support
=============================================================
Voor een B-merk tracker van Ø35 x 8 mm, aan een riem van 15 mm breed.

Een ronde bak met de riemtunnel eronder. De tag klikt van bovenaf in en wordt
vastgehouden door een rondlopende lip. Die lip loopt onder 45 graden naar binnen,
dus elke laag steunt op de vorige -> printbaar zonder support, en zonder brug.

Print-orientatie zit al in de STL: platte onderkant op het bed, opening omhoog.
Het enige wat overbrugd wordt is het dak van de riemtunnel; de bovenhoeken daarvan
zijn onder 45 graden afgeschuind zodat er nog maar ~11 mm vlak te overbruggen is.

De wand heeft 4 veersleuven, zodat de rand naar buiten kan veren als je de tag
erin drukt. Aan een kant zit een duimuitsparing om hem er weer uit te duwen.

Maten in mm. Z=0 = kant tegen de kat, Z omhoog = van de kat af.
"""
import numpy as np
import trimesh
from shapely.geometry import box as sbox

ENGINE = "manifold"

# ============================================================
#  PARAMETERS  -- meet je eigen tag/riem na!
# ============================================================
TAG_D      = 35.0   # diameter van de tag (METEN)
TAG_H      = 8.0    # dikte van de tag (METEN)
SPEL_D     = 0.6    # speling op de diameter (totaal, dus 0,3 per zijde)
SPEL_H     = 0.15   # speling op de dikte (lip drukt de tag licht aan)

WAND       = 1.8    # wanddikte van de bak
BODEM      = 1.4    # bodem van de tagholte = dak van de riemtunnel

LIP        = 1.1    # hoeveel de lip over de tag valt (groter = houdt steviger,
                    #   maar moeilijker inklikken).  Opening wordt TAG_D - 2*LIP
LIP_HELLING = 0.9   # dr/dz van de lip; 1.0 = 45 graden. Lager = flauwer = veiliger

SLEUF_B    = 15.0   # riemsleuf breedte
SLEUF_H    = 8.0    # riemsleuf hoogte
SLEUF_R    = 1.5    # afronding onderhoeken sleuf
SLEUF_SCHUIN = 2.0  # 45-graden afschuining bovenhoeken -> kortere brug
LUS_WAND   = 4.0    # materiaal naast de sleuf
BRUG_DIK   = 1.4    # materiaal onder de sleuf (kant van de kat)
UITSTEEK   = 5.0    # hoever de tunnel buiten de ronde bak uitsteekt (per zijde)

N_VEER     = 4      # veersleuven in de wand (0 = geen)
VEER_B     = 2.5    # breedte veersleuf
VEER_ONDER = 1.4    # hoeveel wand er onder de veersleuf blijft staan (scharnier)

DUIM_B     = 14.0   # duimuitsparing om de tag eruit te duwen (0 = geen)
DUIM_DIEP  = 4.6    # hoever de uitsparing onder de bovenrand doorloopt

RAND_AFSCH = 0.6    # afschuining buitenste bovenrand (geen scherpe kant)
ONDER_AFSCH = 0.8   # afschuining onderrand, kant van de kat

QS = 128            # segmenten in de ronde delen

# ============================================================
#  AFGELEIDE MATEN
# ============================================================
R_HOLTE = TAG_D/2 + SPEL_D/2           # 17.80  binnenmaat tagholte
R_BUI   = R_HOLTE + WAND               # 19.60  buitenradius
R_LIP   = R_HOLTE - LIP                # 16.70  vrije opening (straal)

z_sleuf0 = BRUG_DIK                    #  1.40
z_sleuf1 = z_sleuf0 + SLEUF_H          #  9.40
z_vloer  = z_sleuf1 + BODEM            # 10.80  bodem van de tagholte
z_lip0   = z_vloer + TAG_H + SPEL_H    # 18.95  hier begint de lip
z_top    = z_lip0 + LIP/LIP_HELLING    # 20.17  bovenrand

BAR_L = 2*R_BUI + 2*UITSTEEK           # 49.20  lengte van de riemtunnel
BAR_B = SLEUF_B + 2*LUS_WAND           # 23.00  breedte van de riemtunnel


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
    if m.volume < 0:                      # profiel andersom rond -> normalen om
        m.invert()
    return m


def kegel(r0, r1, za, zb):
    """Afgeknotte kegel: r0 @ za -> r1 @ zb."""
    return wentel([(0.0, za), (r0, za), (r1, zb), (0.0, zb)])


def box(w, d, za, zb, x=0.0, y=0.0):
    b = trimesh.creation.box(extents=[w, d, zb-za])
    b.apply_translation([x, y, (za+zb)/2])
    return b


def prisma_x(poly, L, xc=0.0):
    """Prisma met de as in X; poly is de doorsnede in (z, y)."""
    m = trimesh.creation.extrude_polygon(poly, height=L)
    m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi/2, [0, 1, 0]))
    m.apply_translation([L/2 + xc, 0, 0])
    return m


def afgeronde_balk(L, B, za, zb, hoek=6.0, afschuin=0.0, stappen=4):
    """Balk met afgeronde hoeken; getrapte afschuining aan de onderkant."""
    poly = sbox(-L/2, -B/2, L/2, B/2).buffer(-hoek).buffer(hoek, join_style=1)
    if afschuin <= 0:
        m = trimesh.creation.extrude_polygon(poly, height=zb-za)
        m.apply_translation([0, 0, za])
        return m
    h = afschuin/stappen
    delen = []
    for i in range(stappen):
        s = trimesh.creation.extrude_polygon(
                poly.buffer(-afschuin*(stappen-i)/stappen), height=h+0.01)
        s.apply_translation([0, 0, za + i*h])
        delen.append(s)
    romp = trimesh.creation.extrude_polygon(poly, height=zb-za-afschuin)
    romp.apply_translation([0, 0, za+afschuin])
    return U(delen + [romp])


def sleuf_snijder(L):
    """De riemsleuf: onderhoeken rond, bovenhoeken 45 graden -> korte brug."""
    b, h, s = SLEUF_B/2, SLEUF_H, SLEUF_SCHUIN
    # doorsnede in (z, y); z loopt van 0 (onder) naar h (boven)
    pts = [(0.0, -b), (h - s, -b), (h, -b + s), (h, b - s), (h - s, b), (0.0, b)]
    poly = trimesh.path.polygons.Polygon(pts)
    poly = poly.buffer(-SLEUF_R).buffer(SLEUF_R, join_style=1)   # hoeken breken
    m = prisma_x(poly, L)
    m.apply_translation([0, 0, z_sleuf0])
    return m


# ============================================================
#  HET MODEL
# ============================================================
def maak_houder():
    # --- massieve romp: riemtunnel-balk + 45-graden overgang + ronde bak
    balk  = afgeronde_balk(BAR_L, BAR_B, 0.0, z_vloer, hoek=6.0, afschuin=ONDER_AFSCH)
    flare = kegel(BAR_B/2, R_BUI, z_vloer - (R_BUI - BAR_B/2), z_vloer)
    bak   = wentel([
        (0.0,   z_vloer - 0.01),
        (R_BUI, z_vloer - 0.01),
        (R_BUI, z_top - RAND_AFSCH),
        (R_BUI - RAND_AFSCH, z_top),      # gebroken buitenrand (45 gr., printbaar)
        (0.0,   z_top),
    ])
    romp = U([balk, flare, bak])

    # --- riemtunnel eruit
    romp = D(romp, sleuf_snijder(BAR_L + 6))

    # --- tagholte met lip erboven: wand loopt onder 45 gr. naar binnen
    holte = wentel([
        (0.0,     z_vloer),
        (R_HOLTE, z_vloer),
        (R_HOLTE, z_lip0),
        (R_LIP,   z_top),                 # de lip zelf
        (0.0,     z_top + 1.0),
        (0.0,     z_vloer),
    ])
    romp = D(romp, holte)

    # --- veersleuven zodat de rand naar buiten kan wijken bij het inklikken
    if N_VEER:
        sleuven = []
        for a in np.linspace(0, 2*np.pi, N_VEER, endpoint=False) + np.pi/4:
            s = box(5.0, VEER_B, z_vloer + VEER_ONDER, z_top + 1.0, x=R_HOLTE)
            s.apply_transform(trimesh.transformations.rotation_matrix(a, [0, 0, 1]))
            sleuven.append(s)
        romp = D(romp, U(sleuven))

    # --- duimuitsparing (haaks op de riem) om de tag eruit te duwen
    if DUIM_B > 0:
        pts = [(0.0, -DUIM_B/2), (0.0, DUIM_B/2),
               (DUIM_DIEP + 2.0, DUIM_B/2), (DUIM_DIEP + 2.0, -DUIM_B/2)]
        poly = trimesh.path.polygons.Polygon(pts).buffer(-2.0).buffer(2.0, join_style=1)
        duim = prisma_x(poly, 12.0, xc=R_HOLTE - 2.0)
        duim.apply_translation([0, 0, z_top - DUIM_DIEP])
        duim.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 0, 1]))
        romp = D(romp, duim)

    return romp


def tag_dummy():
    c = trimesh.creation.cylinder(radius=TAG_D/2, height=TAG_H, sections=QS)
    c.apply_translation([0, 0, z_vloer + TAG_H/2])
    return c


if __name__ == "__main__":
    m = maak_houder()
    m.export("airtag_houder.stl")
    print(f"HOUDER: dicht={m.is_watertight} delen={m.body_count} "
          f"bbox={np.round(m.extents,2)} volume={m.volume/1000:.2f} cm3 "
          f"(~{m.volume*1.27/1000:.1f} g PETG massief)")
    print(f"  hoogte {z_top:.2f} mm  |  boven de riem {z_top - z_sleuf1:.2f} mm  |  "
          f"buitenmaat {BAR_L:.1f} x {2*R_BUI:.1f} mm")
    print(f"  tagholte Ø{2*R_HOLTE:.1f} x {TAG_H+SPEL_H:.2f}  |  "
          f"opening Ø{2*R_LIP:.1f}  |  lip {LIP:.1f} mm, overstek "
          f"{np.degrees(np.arctan(LIP_HELLING)):.0f}° uit het lood (<45 = printbaar)")
