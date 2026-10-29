"""Haakje voor sierverlichting, bevestigd met een bout door het midden in de schroefdraadgaten
(vliegtuigboxen) van de Kangoo. Draadmaat onbekend, dus een set: M5, M6, M8, M10.
Print plat (voet op het bed): lagen lopen mee met de haak = sterkst. Alle maten in mm."""
import numpy as np, trimesh, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

# naam: (doorlaatgat, kopuitsparing-diameter, kophoogte cilinderkop)
MATEN = {"M5": (5.5, 9.5, 5.0), "M6": (6.6, 11.5, 6.0),
         "M8": (8.6, 14.5, 8.0), "M10": (11.0, 17.5, 10.0)}
VLOER = 3.5   # materiaal onder de boutkop
ARM_B = 7.0

def maak(naam):
    gat_d, kop_d, kop_h = MATEN[naam]
    kop_diepte = kop_h + 0.5
    dikte = kop_diepte + VLOER
    schijf_r = max(13.0, kop_d/2 + 4.5)
    pad = [(0,0),(0,24)]
    pad += [(8+8*np.cos(a), 24+8*np.sin(a)) for a in np.linspace(np.pi, 0, 30)] + [(16,17)]
    profiel = unary_union([LineString(pad).buffer(ARM_B/2, resolution=24),
                           Point(0,0).buffer(schijf_r, resolution=48)])
    body = trimesh.creation.extrude_polygon(profiel, dikte)
    gat = trimesh.creation.cylinder(radius=gat_d/2, height=dikte*3, sections=64)
    kop = trimesh.creation.cylinder(radius=kop_d/2, height=kop_diepte*2, sections=64)
    kop.apply_translation([0,0,dikte])
    mesh = trimesh.boolean.difference([body, gat, kop], engine="manifold")
    mesh.export(f"kangoo_haakje_{naam}.stl")
    print(naam, "watertight", mesh.is_watertight, "bbox", mesh.extents.round(1), "dikte", dikte)
    return profiel, mesh, gat_d

fig, ax = plt.subplots(2, 4, figsize=(14,8))
for i, n in enumerate(MATEN):
    p, m, g = maak(n)
    x, y = p.exterior.xy
    ax[0,i].fill(x, y, alpha=.4); ax[0,i].add_patch(plt.Circle((0,0), g/2, color='w'))
    ax[0,i].set_aspect('equal'); ax[0,i].set_title(n)
    for e in m.section(plane_origin=[0,0,0], plane_normal=[0,1,0]).discrete:
        ax[1,i].fill(e[:,0], e[:,2], alpha=.4)
    ax[1,i].set_aspect('equal'); ax[1,i].set_title(f"doorsnede {n}")
plt.tight_layout(); plt.savefig("preview.png", dpi=80)
