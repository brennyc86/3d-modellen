#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AirTag-houder voor een kattentuigje  (B-merk tag: Ø35 x 8 mm)
=============================================================
Twee delen die op elkaar klikken:

  KAP  -- ronde kap met de holte voor de tag (zit aan de buitenkant).
  VOET -- bodemplaat met daaronder een riemtunnel van 15 x 8 mm; klikt in de kap.

De riem van het tuigje gaat dwars door de tunnel, van de ene uitstulping naar de
andere. Daardoor:
  - kan de houder niet draaien of verschuiven op de riem;
  - drukt de riem/de kat de VOET juist *in* de kap -> de klik kan niet openvallen.

De tag laadt van onderaf in: kap eraf klikken, tag erin, voet erop drukken.

Print-orientatie zit al in de STL's:
  KAP  = platte bovenkant op het bed, holte omhoog  -> geen support.
  VOET = tunnelbodem op het bed, plug omhoog        -> geen support
         (het tunneldak is een vlakke brug van 15 mm, dat kan elke printer).

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
SPEL_H     = 0.3    # speling op de dikte

WAND       = 2.0    # wanddikte van de kap
TOP_DIK    = 1.6    # dikte bovenplaat kap (buitenkant)
FLENS_DIK  = 1.6    # dikte bodemplaat = tunneldak
PLUG_H     = 2.4    # hoogte van de klikrand van de voet
PLUG_WAND  = 1.2    # wanddikte klikrand (dun = veert lekker)

SLEUF_B    = 15.0   # riemsleuf breedte
SLEUF_H    = 8.0    # riemsleuf hoogte
SLEUF_R    = 1.5    # hoekafronding in de sleuf
LUS_WAND   = 4.0    # materiaal naast de sleuf
BRUG_DIK   = 1.6    # materiaal onder de sleuf (kant van de kat)
UITSTEEK   = 5.0    # hoever de tunnel buiten de ronde kap uitsteekt (per zijde)

KLIK       = 0.35   # radiale overlap van de kliknok (hoe stug hij vastklikt)
N_SPLEET   = 6      # aantal veersleufjes in de klikrand
SPLEET_B   = 2.0    # breedte veersleufjes

GELUID_D   = 3.0    # geluidsgaatjes in de bovenplaat (0 = geen gaatjes)
GELUID_N   = 6      # aantal gaatjes op een cirkel + 1 in het midden
GELUID_R   = 10.0   # cirkel waarop de gaatjes liggen

NOKJES     = True   # 3 bultjes tegen de bovenplaat -> tag rammelt niet
NOK_H      = 0.45
NOK_D      = 3.0

OOR_UIT    = 1.0    # 2 duimnageltjes op de flens om de kap open te wippen
OOR_B      = 11.0

QS = 128            # segmenten in de ronde delen

# ============================================================
#  AFGELEIDE MATEN
# ============================================================
R_HOLTE = TAG_D/2 + SPEL_D/2          # 17.80  binnenmaat tag
R_ZIT   = R_HOLTE + 0.15              # 17.95  boring waarin de klikrand valt
R_BUI   = R_HOLTE + WAND              # 19.80  buitenradius van de houder
H_HOLTE = TAG_H + SPEL_H              # 8.30

z0        = 0.0                        # onderkant tunnel (tegen de kat)
z_sleuf0  = BRUG_DIK                   # 1.60
z_sleuf1  = z_sleuf0 + SLEUF_H         # 9.60
z_flens1  = z_sleuf1 + FLENS_DIK       # 11.20  naad tussen voet en kap
z_plug1   = z_flens1 + PLUG_H          # 13.60  bovenkant klikrand = bodem tagholte
z_holte1  = z_plug1 + H_HOLTE          # 21.90
z_top     = z_holte1 + TOP_DIK         # 23.50  buitenkant

R_PLUG_BUI = R_HOLTE                   # 17.80  buitenkant klikrand (0,15 speling)
R_PLUG_BIN = R_PLUG_BUI - PLUG_WAND    # 16.60

R_NOK      = R_ZIT + KLIK              # 18.30  top van de nok op de voet
R_GROEF    = R_NOK + 0.10              # 18.40  groef in de kap (0,1 lucht)

z_nok0, z_nok1 = z_flens1 + 1.2, z_flens1 + 1.8   # 12.40 .. 13.00

BAR_L = 2*R_BUI + 2*UITSTEEK           # 49.60  lengte van de riemtunnel
BAR_B = SLEUF_B + 2*LUS_WAND           # 23.00  breedte van de riemtunnel


# ============================================================
#  HULPJES
# ============================================================
def U(ms):  return trimesh.boolean.union(ms, engine=ENGINE)
def D(a, b): return trimesh.boolean.difference([a, b], engine=ENGINE)


def wentel(profiel):
    """Gesloten 2D-profiel (r, z) rondwentelen om de Z-as."""
    p = np.asarray(profiel, dtype=float)
    if not np.allclose(p[0], p[-1]):
        p = np.vstack([p, p[0]])
    m = trimesh.creation.revolve(p, sections=QS)
    m.merge_vertices()
    if m.volume < 0:            # profiel andersom rond -> normalen omkeren
        m.invert()
    return m


def cyl(r, za, zb, x=0.0, y=0.0):
    c = trimesh.creation.cylinder(radius=r, height=zb-za, sections=QS)
    c.apply_translation([x, y, (za+zb)/2])
    return c


def kegel(r0, r1, za, zb):
    """Afgeknotte kegel: r0 @ za -> r1 @ zb."""
    return wentel([(0.0, za), (r0, za), (r1, zb), (0.0, zb)])


def box(w, d, za, zb, x=0.0, y=0.0):
    b = trimesh.creation.box(extents=[w, d, zb-za])
    b.apply_translation([x, y, (za+zb)/2])
    return b


def afgeronde_balk(L, B, za, zb, hoek=6.0, afschuin=0.0, stappen=4):
    """Balk met afgeronde hoeken; optioneel een getrapte afschuining onderaan."""
    poly = sbox(-L/2, -B/2, L/2, B/2).buffer(-hoek).buffer(hoek, join_style=1)
    if afschuin <= 0:
        m = trimesh.creation.extrude_polygon(poly, height=zb-za)
        m.apply_translation([0, 0, za])
        return m
    # getrapte afschuining onderaan (kant van de kat): geen scherpe rand
    h = afschuin/stappen
    delen = []
    for i in range(stappen):
        p = poly.buffer(-afschuin*(stappen-i)/stappen)
        s = trimesh.creation.extrude_polygon(p, height=h+0.01)
        s.apply_translation([0, 0, za + i*h])
        delen.append(s)
    romp = trimesh.creation.extrude_polygon(poly, height=zb-za-afschuin)
    romp.apply_translation([0, 0, za+afschuin])
    return U(delen + [romp])


def sleuf_profiel(L):
    """De riemsleuf als balk met afgeronde hoeken, liggend in X."""
    # na de rotatie om Y geldt: poly-x -> Z (hoogte), poly-y -> Y (breedte)
    poly = sbox(-SLEUF_H/2, -SLEUF_B/2, SLEUF_H/2, SLEUF_B/2) \
             .buffer(-SLEUF_R).buffer(SLEUF_R, join_style=1)
    m = trimesh.creation.extrude_polygon(poly, height=L)
    # extrusie staat in +Z: kantelen zodat de lengte in X ligt
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [0, 1, 0]))
    m.apply_translation([-L/2, 0, (z_sleuf0+z_sleuf1)/2])
    return m


# ============================================================
#  DEEL 1 -- KAP
# ============================================================
def maak_kap():
    ronding = 2.0
    boog = [(R_HOLTE + ronding*np.sin(a), z_top - ronding + ronding*np.cos(a))
            for a in np.linspace(0, np.pi/2, 12)]

    profiel = [
        (R_NOK + 0.15, z_flens1),     # oploop aan de onderrand: klikt makkelijk in
        (R_ZIT,   z_flens1 + 0.8),    # boring waarin de klikrand valt
        (R_ZIT,   z_nok0 - 0.25),
        (R_GROEF, z_nok0),            # klikgroef: steile kant = vasthouden
        (R_GROEF, z_nok1),
        (R_ZIT,   z_nok1 + 0.55),     # flauwe kant = makkelijk indrukken
        (R_ZIT,   z_plug1),
        (R_HOLTE, z_plug1),           # stap naar de tagholte
        (R_HOLTE, z_holte1),
        (0.0,     z_holte1),          # plafond van de holte
        (0.0,     z_top),
        *boog,                        # afgeronde bovenrand (r=2)
        (R_BUI,   z_flens1),          # buitenwand omlaag
    ]
    kap = wentel(profiel)

    if NOKJES:                        # bultjes tegen rammelen
        bult = [cyl(NOK_D/2, z_holte1 - NOK_H, z_holte1,
                    x=12.0*np.cos(a), y=12.0*np.sin(a))
                for a in np.deg2rad([90, 210, 330])]
        kap = U([kap] + bult)

    if GELUID_D > 0:                  # geluid/uitdruk-gaatjes
        gaten = [cyl(GELUID_D/2, z_holte1 - 1, z_top + 1)]
        gaten += [cyl(GELUID_D/2, z_holte1 - 1, z_top + 1,
                      x=GELUID_R*np.cos(a), y=GELUID_R*np.sin(a))
                  for a in np.linspace(0, 2*np.pi, GELUID_N, endpoint=False)]
        kap = D(kap, U(gaten))

    return kap


# ============================================================
#  DEEL 2 -- VOET (bodemplaat + riemtunnel)
# ============================================================
def maak_voet():
    # riemtunnel-balk, met een 45-graden overgang naar de ronde flens
    balk = afgeronde_balk(BAR_L, BAR_B, z0, z_flens1, hoek=6.0, afschuin=0.8)
    flare = kegel(BAR_B/2, R_BUI, z_flens1 - (R_BUI - BAR_B/2), z_flens1)
    flens = cyl(R_BUI, z_sleuf1, z_flens1)

    # duimnageltjes om de kap eraf te wippen (haaks op de riem)
    oren = trimesh.boolean.intersection(
        [U([box(OOR_B, 2*(R_BUI+OOR_UIT), z_sleuf1, z_flens1)]),
         cyl(R_BUI + OOR_UIT, z_sleuf1, z_flens1)], engine=ENGINE)

    # klikrand
    plug = wentel([
        (R_PLUG_BUI, z_flens1),
        (R_PLUG_BUI, z_nok0 - 0.25),
        (R_NOK,      z_nok0),
        (R_NOK,      z_nok1),
        (R_PLUG_BUI, z_nok1 + 0.45),   # oploop: makkelijk indrukken
        (R_PLUG_BUI, z_plug1),
        (R_PLUG_BIN, z_plug1),
        (R_PLUG_BIN, z_flens1),
    ])

    voet = U([balk, flare, flens, oren, plug])
    voet = D(voet, sleuf_profiel(BAR_L + 4))

    # veersleufjes in de klikrand
    spleten = []
    for a in np.linspace(0, 2*np.pi, N_SPLEET, endpoint=False) + np.pi/N_SPLEET:
        # radiaal helemaal door de klikrand, maar niet tot in de flensrand
        s = box(3.5, SPLEET_B, z_flens1 - 0.4, z_plug1 + 0.5, x=R_PLUG_BIN + 0.65)
        s.apply_transform(trimesh.transformations.rotation_matrix(a, [0, 0, 1]))
        spleten.append(s)
    voet = D(voet, U(spleten))
    return voet


# ============================================================
def tag_dummy():
    return cyl(TAG_D/2, z_plug1, z_plug1 + TAG_H)


if __name__ == "__main__":
    kap, voet = maak_kap(), maak_voet()

    # print-orientatie: kap ondersteboven, voet zoals hij is
    kap_p = kap.copy()
    kap_p.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    kap_p.apply_translation([0, 0, -kap_p.bounds[0][2]])
    voet_p = voet.copy()
    voet_p.apply_translation([0, 0, -voet_p.bounds[0][2]])

    kap_p.export("airtag_kap.stl")
    voet_p.export("airtag_voet.stl")

    for naam, m in (("KAP ", kap), ("VOET", voet)):
        print(f"{naam}: dicht={m.is_watertight} bbox={np.round(m.extents,2)} "
              f"volume={m.volume/1000:6.2f} cm3  ~{m.volume*1.24/1000:5.1f} g PLA  "
              f"tris={len(m.faces)}")
    tot = kap.volume + voet.volume
    print(f"TOTAAL: hoogte {z_top:.1f} mm, {BAR_L:.1f} x {2*R_BUI:.1f} mm, "
          f"~{tot*1.24/1000:.1f} g PLA / {tot*1.27/1000:.1f} g PETG")
