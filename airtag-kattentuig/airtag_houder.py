#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AirTag-houder voor een kattentuigje -- EEN STUK, TPU, geen support
==================================================================
Voor een B-merk tracker van Ø35 x 8 mm.

Een ronde bak met aan weerszijden een platte uitstulping met een gat van 15 x 8 mm
(15 x 8 omdat de sluitclip van het tuigje er ook doorheen moet). Het gat staat
RECHTOP, dus er wordt nergens iets overbrugd. Je weeft het tuigje er zelf doorheen
en kiest zelf of de riem onder of boven de houder langs loopt.

De tag wordt van bovenaf onder een rondlopende lip gedrukt. Eruit duw je hem door
het gat in de bodem.

ALLE randen zijn afgerond, ook aan de binnenkant rond de tag -- die is zelf ook
rond, dus de lip volgt zijn vorm. Overal is de vorm zo gekozen dat de overhang
onder de 45 graden blijft:
  - naar binnen omlopende vlakken (de lip) staan op 39 graden;
  - alle afrondingen zitten bovenaan een vlak, waar elke laag op de vorige rust;
  - de bedzijde begint met een recht stukje van precies 45 graden en buigt daarna
    met een ruime radius de wand in: het rondste wat op laag 1 kan zonder om te
    krullen.

Print-orientatie zit al in de STL: platte onderkant op het bed, opening omhoog.

Maten in mm. Z=0 = kant tegen de kat, Z omhoog = van de kat af.
"""
import numpy as np
import trimesh
import shapely
from shapely.geometry import box as sbox, Point, Polygon
from shapely.ops import unary_union

ENGINE = "manifold"

# ============================================================
#  PARAMETERS  -- meet je eigen tag/riem na!
# ============================================================
TAG_D      = 35.0   # diameter van de tag (METEN)
TAG_H      = 8.0    # dikte van de tag (METEN)
SPEL_D     = 0.4    # speling op de diameter (TPU: krap mag, het rekt)
SPEL_H     = 0.15   # speling op de dikte

WAND       = 3.0    # wanddikte van de bak
BODEM      = 2.6    # dikte van de bodem

LIP        = 2.2    # hoeveel de lip over de tag valt
LIP_HELLING = 0.8   # dr/dz van de lip; 1.0 = 45 gr. 0.8 = 39 gr = veilig voor TPU

# --- afrondingen -------------------------------------------------------------
ROND_RAND  = 4.0    # bovenrand van de bak: de hele wanddikte rondgezet
ROND_LIP   = 1.8    # onderkant van de lip: vloeit in de wand van de tagholte
ROND_TIP   = 1.0    # binnenrand bovenaan, waar de lip over de tag valt
ROND_VLOER = 0.8    # binnenhoek onderin de tagholte
ROND_TAB   = 1.4    # bovenrand van de uitstulpingen
# De bedzijde ligt tegen de kat aan en is daarom zo rond mogelijk gemaakt. Een
# echte afronding kan daar niet: laag 1 zou als een flintertje beginnen en
# omkrullen. Wat wel kan is een LANGE aanloop: hij begint op laag 1 met precies
# 45 graden en buigt daarna met een ruime radius de wand in. Hoe groter deze twee
# getallen, hoe verder de rand van de kat wegrolt.
# De ronde bak krijgt een veel ruimere aanloop dan de uitstulpingen: die is maar
# 4,4 mm dik, daar past zo'n bocht simpelweg niet in. Vandaar twee stellen maten.
AFSCH_BAK  = 3.5    # bak: inzet van de omtrek op laag 1
ROND_BAK   = 11.9   # bak: radius van de aanloop (max = 3,41 x de inzet)

AFSCH_ONDER = 1.6   # uitstulpingen: inzet van de omtrek op laag 1
ROND_ONDER = 3.2    # uitstulpingen: radius waarmee die aanloop de wand in buigt

# De riemgaten raken de kat niet, dus die krijgen een kleinere aanloop -- anders
# blijft er tussen gat en rand van de uitstulping te weinig materiaal over.
AFSCH_GAT  = 0.6
ROND_GAT   = 1.2
ROND_GAT_TOP = 0.8  # afronding van de bovenrand van de riemgaten
AFSCH_DRUK = 1.0    # aanloop rond het uitduwgat, ook aan de kant van de kat
ROND_DRUK  = 1.8

# --- uitstulpingen -----------------------------------------------------------
UITSTULP_B = 22.0   # breedte van de uitstulpingen
UITSTULP_D = 4.4    # dikte van de uitstulpingen (past de hele aanloop in)
GAT_B      = 15.0   # gat: breedte (dwars op de riem)
GAT_L      = 8.0    # gat: lengte (in de looprichting) -- de sluitclip moet erdoor
GAT_R      = 1.5    # afronding hoeken van het gat
RAND_BIN   = 2.5    # materiaal tussen de bak en het gat
RAND_BUI   = 4.0    # materiaal tussen het gat en het uiteinde
EIND_R     = 5.0    # afronding van de hoeken van de uitstulping
FILET      = 3.0    # afronding waar de uitstulping in de bak overgaat

# --- dubbel oog aan een van de twee vrije kanten -----------------------------
# Twee openingen van dezelfde maat, met een steg ertussen. De riem gaat door de
# ene omhoog en door de andere terug omlaag, om de steg heen -- zoals een
# tri-glide. Daarmee klem je de houder op een kort stuk riem in plaats van dat
# hij een rechte baan van 70 mm nodig heeft tussen de twee losse ogen.
DUBBEL_OOG = True
OOG_KANT   = 1      # 1 = aan de +Y kant, -1 = aan de -Y kant
RAND_MID   = 3.5    # steg tussen de twee openingen (daar loopt de riem omheen)

DRUK_D     = 20.0   # gat in de bodem om de tag eruit te duwen (0 = dicht)

# Meshfijnheid. Ruimer dan dit is verspilling: bij QS=80 is de koordafwijking op
# Ø41 nog geen 0,02 mm, ver onder wat een printer kan. Grover scheelt vooral in
# bestandsgrootte -- en GitHub weigert grote STL's te tonen.
QS   = 64           # segmenten in de ronde delen
NB   = 8            # punten per afronding in een omwentelingsprofiel
NR_ROND = 7         # facetten per afronding in de rand van de uitstulpingen
STAP = 2.0          # afstand tussen de punten op een gelofte rand (mm)

# ============================================================
#  AFGELEIDE MATEN
# ============================================================
R_HOLTE = TAG_D/2 + SPEL_D/2           # 17.70  binnenmaat tagholte
R_BUI   = R_HOLTE + WAND               # 20.10  buitenradius van de bak
R_LIP   = R_HOLTE - LIP                # 15.50  vrije opening (straal)

ALFA    = np.arctan(LIP_HELLING)       # 38.66 gr. -- hoek van de lip uit het lood
z_lip0  = BODEM + TAG_H + SPEL_H       #  9.95  hier begint de lip aan te lopen

# opbouw van het lipprofiel: wand -> afronding -> schuin vlak -> afronding -> top
_A_r    = R_HOLTE - ROND_LIP + ROND_LIP*np.cos(ALFA)   # eind van de onderafronding
_A_z    = z_lip0 + ROND_LIP*np.sin(ALFA)
_T_r    = R_LIP + ROND_TIP*(1 - np.cos(ALFA))          # eind van het schuine vlak
_T_z    = _A_z + (_A_r - _T_r)/LIP_HELLING
z_top   = _T_z + ROND_TIP*(1 + np.sin(ALFA))           # bovenrand van de bak
_C2_r   = R_LIP + ROND_TIP                             # hart van de tip-afronding

GAT_X0  = R_BUI + RAND_BIN             # binnenkant gat
GAT_X1  = GAT_X0 + GAT_L               # buitenkant gat
TOT_L   = 2*(GAT_X1 + RAND_BUI)        # totale lengte over de twee losse ogen

OOG_Y0  = R_BUI + RAND_BIN             # dubbel oog: binnenkant eerste opening
OOG_Y1  = OOG_Y0 + GAT_L
OOG_Y2  = OOG_Y1 + RAND_MID            # steg
OOG_Y3  = OOG_Y2 + GAT_L
OOG_EIND = OOG_Y3 + RAND_BUI           # uiteinde van het dubbele oog


# ============================================================
#  HULPJES
# ============================================================
def U(ms):   return trimesh.boolean.union(ms, engine=ENGINE)
def D(a, b): return trimesh.boolean.difference([a, b], engine=ENGINE)


def boog(cr, cz, r, a0, a1, n=NB):
    """Punten op een cirkelboog, hoeken in graden."""
    t = np.radians(np.linspace(a0, a1, n))
    return list(zip(cr + r*np.cos(t), cz + r*np.sin(t)))


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


def _ringen(poly):
    """Buitenrand + gaten van een polygoon, altijd in dezelfde volgorde."""
    p = shapely.geometry.polygon.orient(poly, 1.0)
    binnen = sorted(p.interiors, key=lambda r: (round(r.centroid.x, 3),
                                               round(r.centroid.y, 3)))
    return [p.exterior] + list(binnen)


def _bemonster(ring, n):
    """n punten gelijk verdeeld over een ring, startend bij het punt uiterst +X."""
    L = ring.length
    pts = np.array([ring.interpolate(i*L/n).coords[0] for i in range(n)])
    return np.roll(pts, -int(np.argmax(pts[:, 0])), axis=0)


def _volg(ring, punten):
    """Zoek op `ring` de punten die het dichtst bij `punten` liggen, in dezelfde
    volgorde. Zo lopen de facetten van een gelofte rand mooi loodrecht mee in
    plaats van scheef weg te lopen bij de bochten."""
    t = np.array([ring.project(Point(p)) for p in punten])
    t = t[0] + np.maximum.accumulate(np.unwrap(t - t[0], period=ring.length))
    return np.array([ring.interpolate(v % ring.length).coords[0] for v in t])


def gelofte(buiten, gaten, prof_buiten, prof_gaten):
    """Plaat waarvan de omtrek en de gaten elk hun eigen randprofiel krijgen. De
    omtrek wordt tussen de niveaus doorgelofd, dus een echte schuine/ronde rand
    zonder de trapjes die je krijgt als je plakjes op elkaar stapelt."""
    def vlak(z):
        d_b = np.interp(z, prof_buiten[:, 0], prof_buiten[:, 1])
        d_g = np.interp(z, prof_gaten[:, 0], prof_gaten[:, 1])
        p = buiten.buffer(-d_b, join_style=1) if d_b > 1e-9 else buiten
        return p.difference(gaten.buffer(d_g, join_style=1) if d_g > 1e-9 else gaten)

    ruw = np.unique(np.round(np.r_[prof_buiten[:, 0], prof_gaten[:, 0]], 6))
    hoogtes = ruw[np.r_[True, np.diff(ruw) > 0.12]]      # te dicht op elkaar = zonde
    basis = _ringen(vlak(hoogtes[len(hoogtes)//2]))
    n_pt = [max(48, int(np.ceil(r.length/STAP))) for r in basis]
    anker = [_bemonster(r, n) for r, n in zip(basis, n_pt)]

    lagen = []
    for z in hoogtes:
        ringen = _ringen(vlak(z))
        assert len(ringen) == len(basis), "rand valt uit elkaar: inzet te groot"
        lagen.append([np.c_[_volg(r, a), np.full(len(a), z)]
                      for r, a in zip(ringen, anker)])

    verts, faces, offset = [], [], 0
    for k, n in enumerate(n_pt):                       # zijwanden tussen de niveaus
        for a, b in zip(lagen[:-1], lagen[1:]):
            verts += [a[k], b[k]]
            for i in range(n):
                j = (i+1) % n
                faces += [[offset+i, offset+j, offset+n+i],
                          [offset+j, offset+n+j, offset+n+i]]
            offset += 2*n

    for laag in (lagen[0], lagen[-1]):                 # deksel onder en boven
        vlak = Polygon(laag[0][:, :2], [r[:, :2] for r in laag[1:]])
        v2, f2 = trimesh.creation.triangulate_polygon(vlak, engine="earcut")
        verts.append(np.c_[v2, np.full(len(v2), laag[0][0, 2])])
        faces += (np.asarray(f2) + offset).tolist()
        offset += len(v2)

    m = trimesh.Trimesh(vertices=np.vstack(verts), faces=np.array(faces))
    m.merge_vertices()
    m.fix_normals()
    return m


# ============================================================
#  HET MODEL
# ============================================================
def tabplattegrond():
    """Alleen de uitstulpingen, met een schijf ter grootte van de smalste maat van
    de bak eronder. Die schijf zit altijd bínnen de bak (de bak wordt naar boven
    toe breder), dus hij overschrijft de ronding van de bak niet, maar geeft de
    overgang bak <-> uitstulping wel een nette filet."""
    vorm = Point(0, 0).buffer(R_BUI - AFSCH_BAK, resolution=QS//4)
    for teken in (1, -1):
        eind = teken * (GAT_X1 + RAND_BUI)
        lip = sbox(min(0, eind), -UITSTULP_B/2, max(0, eind), UITSTULP_B/2)
        vorm = vorm.union(lip.buffer(-EIND_R).buffer(EIND_R, join_style=1))
    if DUBBEL_OOG:
        eind = OOG_KANT * OOG_EIND
        lip = sbox(-UITSTULP_B/2, min(0, eind), UITSTULP_B/2, max(0, eind))
        vorm = vorm.union(lip.buffer(-EIND_R).buffer(EIND_R, join_style=1))
    return vorm.buffer(FILET, join_style=1).buffer(-FILET, join_style=1)


def _rond_gat(x0, y0, x1, y1):
    return sbox(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)) \
             .buffer(-GAT_R).buffer(GAT_R, join_style=1)


def riemgaten():
    """Alle rechtopstaande riemgaten, als 2D-vorm."""
    g = [_rond_gat(t*GAT_X0, -GAT_B/2, t*GAT_X1, GAT_B/2) for t in (1, -1)]
    if DUBBEL_OOG:
        k = OOG_KANT
        g += [_rond_gat(-GAT_B/2, k*OOG_Y0, GAT_B/2, k*OOG_Y1),
              _rond_gat(-GAT_B/2, k*OOG_Y2, GAT_B/2, k*OOG_Y3)]
    return unary_union(g)


def aanloop(inzet, radius):
    """Bedzijde als [(z, inzet), ...]: een recht stuk van precies 45 graden dat
    met `radius` de verticale wand in buigt. Nergens steiler dan 45 graden, maar
    het rolt over `z_eind` mm van de kat weg in plaats van over een scherpe kant."""
    z_eind = inzet + radius*(np.sqrt(2) - 1)             # daar staat de wand recht
    z_knik = z_eind - radius*np.sqrt(0.5)                # eind van het rechte 45-stuk
    nv = [(0.0, inzet), (z_knik, inzet - z_knik)]
    for f in np.radians(np.linspace(-45, 0, NR_ROND))[1:]:
        nv.append((z_eind + radius*np.sin(f), radius*(1 - np.cos(f))))
    return nv


def bovenrond(radius):
    """Afronding van de bovenrand van een plaat, als [(z, inzet), ...]."""
    return [(UITSTULP_D - radius + t, radius - np.sqrt(max(radius**2 - t**2, 0.0)))
            for t in np.linspace(0, radius, NR_ROND)]


def randprofiel(inzet, radius, top):
    """Volledig randprofiel van onder naar boven, altijd oplopend in z."""
    nv = aanloop(inzet, radius) + [(UITSTULP_D - top, 0.0)] + bovenrond(top)
    return np.array(sorted(nv))


def maak_houder():
    # --- de twee uitstulpingen (de ronde bak zit hier bewust NIET in: die heeft
    #     zijn eigen, veel ruimere aanloop en zou anders overschreven worden)
    onder = gelofte(tabplattegrond(), riemgaten(),
                    randprofiel(AFSCH_ONDER, ROND_ONDER, ROND_TAB),
                    randprofiel(AFSCH_GAT, ROND_GAT, ROND_GAT_TOP))

    # --- de ronde bak: afschuining onderaan, bovenrand helemaal rondgezet
    bak = wentel([
        (0.0, 0.0),
        *[(R_BUI - d, z) for z, d in aanloop(AFSCH_BAK, ROND_BAK)],
        (R_BUI, z_top - ROND_RAND),
        *boog(R_BUI - ROND_RAND, z_top - ROND_RAND, ROND_RAND, 0, 90),
        (0.0, z_top),
    ])
    romp = U([onder, bak])

    # --- tagholte: afgeronde binnenhoek, lip die de ronding van de tag volgt
    holte = wentel([
        (0.0, BODEM),
        (R_HOLTE - ROND_VLOER, BODEM),
        *boog(R_HOLTE - ROND_VLOER, BODEM + ROND_VLOER, ROND_VLOER, -90, 0),
        (R_HOLTE, z_lip0),
        *boog(R_HOLTE - ROND_LIP, z_lip0, ROND_LIP, 0, np.degrees(ALFA)),
        (_T_r, _T_z),
        *boog(_C2_r, z_top - ROND_TIP, ROND_TIP, 180 + np.degrees(ALFA), 90),
        (_C2_r, z_top + 1.0),
        (0.0, z_top + 1.0),
    ])
    romp = D(romp, holte)

    # --- uitduwgat in de bodem, beide randen gebroken
    if DRUK_D > 0:
        rd, br = DRUK_D/2, 0.8
        aan = aanloop(AFSCH_DRUK, ROND_DRUK)
        romp = D(romp, wentel([
            (0.0, -1.0),
            (rd + AFSCH_DRUK + 1.0, -1.0),
            *[(rd + d, z) for z, d in aan],           # zelfde soort aanloop als buiten
            (rd, BODEM - br),
            *boog(rd + br, BODEM - br, br, 180, 90),
            (0.0, BODEM),
        ]))

    return romp


def buitenprofiel():
    """De buitenkant van de bak als (z, r), oplopend in z."""
    pts = [(z, R_BUI - d) for z, d in aanloop(AFSCH_BAK, ROND_BAK)]
    pts.append((z_top - ROND_RAND, R_BUI))
    pts += [(z, r) for r, z in boog(R_BUI - ROND_RAND, z_top - ROND_RAND,
                                    ROND_RAND, 0, 90)]
    return np.array(pts)


def holteprofiel():
    """De binnenkant (tagholte + lip) als (z, r), oplopend in z."""
    pts = [(z, r) for r, z in boog(R_HOLTE - ROND_VLOER, BODEM + ROND_VLOER,
                                   ROND_VLOER, -90, 0)]
    pts.append((z_lip0, R_HOLTE))
    pts += [(z, r) for r, z in boog(R_HOLTE - ROND_LIP, z_lip0, ROND_LIP,
                                    0, np.degrees(ALFA))]
    pts.append((_T_z, _T_r))
    pts += [(z, r) for r, z in boog(_C2_r, z_top - ROND_TIP, ROND_TIP,
                                    180 + np.degrees(ALFA), 90)]
    return np.array(pts)


def wanddikte_rapport(n=400):
    """Dunste plek in de wand van de bak: buitenkant min binnenkant."""
    bui, bin_ = buitenprofiel(), holteprofiel()
    z = np.linspace(BODEM, _T_z, n)
    d = np.interp(z, bui[:, 0], bui[:, 1]) - np.interp(z, bin_[:, 0], bin_[:, 1])
    return d.min(), z[int(np.argmin(d))]


def overhang_rapport(m, grens=46.0):
    """Hoeveel neerwaarts vlak staat er steiler dan `grens` graden? Alles boven
    de 45 zou support vragen; het bedvlak zelf telt niet mee. De grens staat op
    46 en niet op 45, omdat de aanloop aan de bedzijde met opzet precies 45 graden
    is: door afrondingsruis vallen die facetten anders willekeurig net erbuiten."""
    omlaag = (m.face_normals[:, 2] < -1e-6) & (m.triangles[:, :, 2].min(axis=1) > 0.05)
    hoek = np.degrees(np.arcsin(np.clip(-m.face_normals[omlaag, 2], 0, 1)))
    opp = m.area_faces[omlaag]
    return opp[hoek > grens].sum(), opp.sum()


def tag_dummy():
    c = trimesh.creation.cylinder(radius=TAG_D/2, height=TAG_H, sections=QS)
    c.apply_translation([0, 0, BODEM + TAG_H/2])
    return c


if __name__ == "__main__":
    m = maak_houder()
    m.export("airtag_houder.stl")
    print(f"HOUDER: dicht={m.is_watertight} delen={m.body_count} "
          f"bbox={np.round(m.extents, 2)} volume={m.volume/1000:.2f} cm3 "
          f"(~{m.volume*1.21/1000:.1f} g TPU massief)")
    print(f"  {TOT_L:.1f} x {UITSTULP_B:.1f} mm uitstulpingen (dik {UITSTULP_D}), "
          f"bak Ø{2*R_BUI:.1f}, hoogte {z_top:.2f} mm")
    print(f"  tagholte Ø{2*R_HOLTE:.1f} x {TAG_H+SPEL_H:.2f}  |  "
          f"nauwste opening Ø{2*R_LIP:.1f}  |  lip {LIP:.1f} mm onder "
          f"{np.degrees(ALFA):.0f}° uit het lood")
    print(f"  afrondingen: buitenrand r{ROND_RAND}, liponder r{ROND_LIP}, "
          f"liptip r{ROND_TIP}, uitstulping r{ROND_TAB}, bedzijde 45° x {AFSCH_ONDER}")
    print(f"  riemgaten {GAT_L:.0f} x {GAT_B:.0f} mm, rechtop door een uitstulping "
          f"van {UITSTULP_D} mm dik")
    if DUBBEL_OOG:
        print(f"  dubbel oog aan de {'+Y' if OOG_KANT > 0 else '-Y'} kant: 2 openingen "
              f"met een steg van {RAND_MID} mm ertussen, steekt "
              f"{OOG_EIND - R_BUI:.1f} mm buiten de bak uit")
    dun, z_dun = wanddikte_rapport()
    print(f"  wanddikte rond de tagholte: minimaal {dun:.2f} mm (op z={z_dun:.1f}) "
          f"-> {'ruim genoeg' if dun >= 1.6 else 'TE DUN'}")
    slecht, totaal = overhang_rapport(m)
    print(f"  overhangcontrole: {slecht:.2f} mm2 van {totaal:.0f} mm2 neerwaarts vlak "
          f"staat steiler dan 46° -> {'GEEN support nodig' if slecht < 2 else 'LET OP'}")
