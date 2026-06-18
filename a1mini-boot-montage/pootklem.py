#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A1 mini boot-montage -- POOTKLEM
================================
Een klemmetje dat om een pootje van de Bambu Lab A1 mini valt en naast de poot
in het plankje wordt geschroefd. Print er 3 a 4 van en zet ze onder de pootjes
(voor / achter / rechts, evt. ook links). Omdat de pootjes binnen de footprint
van de printer zitten, vallen de schroeven automatisch binnen de footprint -- dus
ook als het plankje een paar cm te kort is vóór/achter.

Werking:
  - De ring valt om het rubberen pootje -> printer kan niet meer schuiven.
  - De poot staat via het gat dóór op het plankje (geen hoogteverschil), dus je
    hoeft niet per se alle 4 de poten te klemmen.
  - Een klein lipje bovenaan grijpt over de bovenrand van het pootje -> houdt 'm
    ook omlaag (anti-optillen bij slagzij). Zet LIP=0 om gewoon te laten zakken.

Maten in mm. METEN: pootdiameter, poothoogte. De rest is veilige default.

Coordinaten: X/Y = vlak op het plankje, Z omhoog. Plankje-bovenkant = Z=0.
"""
import numpy as np
import trimesh
from shapely.geometry import box as sbox

ENGINE = "manifold"

# ============================================================
#  PARAMETERS  -- meet je echte pootje na!
# ============================================================
VOET_D    = 22.0   # diameter rubberen pootje (METEN)
VOET_H    = 8.0    # hoogte van het pootje = wandhoogte van de ring (METEN)
SPELING   = 1.0    # speling tussen pootje en ringwand (per zijde)
WAND      = 4.0    # wanddikte van de ring
LIP       = 1.5    # overstek lipje bovenaan (grijpt over de poot). 0 = uit
LIP_DIK   = 2.0    # dikte/hoogte van het lipje

BASIS_DIK = 4.0    # dikte van de schroefplaat (rondom de poot, op het plankje)
TAB_LEN   = 26.0   # hoe ver de schroeftabs uitsteken naast de poot
SCHROEF_D = 4.5    # doorvoergat houtschroef (M4/4mm houtschroef)
KOP_D     = 9.0    # verzonken kop diameter
KOP_DIEP  = 2.6    # verzonken kop diepte

QS = 64

# ============================================================
ri = VOET_D/2.0 + SPELING          # binnenradius ring
Ro = ri + WAND                     # buitenradius ring
schroef_x = Ro + TAB_LEN/2.0       # x-positie schroeven

def cyl(r, z0, z1, x=0.0, y=0.0, seg=QS):
    h = z1 - z0
    c = trimesh.creation.cylinder(radius=r, height=h, sections=seg)
    c.apply_translation([x, y, z0 + h/2.0])
    return c

def cone(r0, r1, z0, z1, x=0.0, y=0.0):
    # afgeknotte kegel (voor verzonken kop): r0 @ z0  ->  r1 @ z1
    h = z1 - z0
    n = 48
    ang = np.linspace(0, 2*np.pi, n, endpoint=False)
    bottom = np.c_[r0*np.cos(ang), r0*np.sin(ang), np.full(n, z0)]
    top    = np.c_[r1*np.cos(ang), r1*np.sin(ang), np.full(n, z1)]
    verts = np.vstack([bottom, top, [0,0,z0], [0,0,z1]])
    cb, ct = 2*n, 2*n+1
    faces = []
    for i in range(n):
        j = (i+1) % n
        faces += [[i, j, n+i], [j, n+j, n+i]]      # zijwand
        faces += [[cb, j, i]]                        # bodem
        faces += [[ct, n+i, n+j]]                    # top
    m = trimesh.Trimesh(vertices=verts, faces=faces, process=True)
    m.apply_translation([x, y, 0])
    return m

def box(w, d, z0, z1, x=0.0, y=0.0):
    b = trimesh.creation.box(extents=[w, d, z1-z0])
    b.apply_translation([x, y, (z0+z1)/2.0])
    return b

def U(ms): return trimesh.boolean.union(ms, engine=ENGINE)
def D(a,b): return trimesh.boolean.difference([a,b], engine=ENGINE)

def maak_pootklem():
    # schroefplaat: afgeronde rechthoek rond de poot + tabs naar links/rechts
    plL = 2*schroef_x + KOP_D + 8
    plB = 2*Ro
    plaat = trimesh.creation.box(extents=[plL, plB, BASIS_DIK])
    plaat.apply_translation([0, 0, BASIS_DIK/2.0])
    # ring om de poot
    ring = D(cyl(Ro, 0, VOET_H), cyl(ri, -1, VOET_H+1))
    body = U([plaat, ring])
    # lip bovenaan (overstek naar binnen)
    if LIP > 0:
        lip = D(cyl(Ro, VOET_H-LIP_DIK, VOET_H), cyl(ri-LIP, VOET_H-LIP_DIK-1, VOET_H+1))
        body = U([body, lip])
    # poot-gat helemaal vrij (poot staat op het plankje)
    body = D(body, cyl(ri, -1, VOET_H+1))
    # 2 verzonken schroefgaten in de tabs
    cuts = []
    for sx in (-1, 1):
        x = sx*schroef_x
        cuts.append(cyl(SCHROEF_D/2.0, -1, BASIS_DIK+1, x=x))
        cuts.append(cone(SCHROEF_D/2.0, KOP_D/2.0, BASIS_DIK-KOP_DIEP, BASIS_DIK+0.01, x=x))
    body = D(body, U(cuts))
    return body

if __name__ == "__main__":
    m = maak_pootklem()
    m.export("pootklem.stl")
    print(f"POOTKLEM: watertight={m.is_watertight} bbox={np.round(m.extents,1)} "
          f"ri={ri} Ro={Ro} tris={len(m.faces)}")
