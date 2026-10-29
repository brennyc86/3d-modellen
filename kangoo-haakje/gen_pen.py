"""Haakje met gladde pen + kleine ribbel (klik) voor de schroefdraadgaten (vliegtuigboxen) in de Kangoo.
Pen zit los in de kern van het draad (kerndiameter D1), de ribbel haakt een stukje in de draadgroef;
een gleuf in het uiteinde laat de pen even meeveren. Geen draad aangeraakt of beschadigd.
Print met de pen OMHOOG: haakje plat op het bed, geen support (ribbel heeft 45 graden flanken). Maten in mm."""
import numpy as np, trimesh, manifold3d as m3, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

DRAAD   = {"M3": (3.0, 0.5), "M4": (4.0, 0.7), "M5": (5.0, 0.8), "M6": (6.0, 1.0), "M8": (8.0, 1.25)}
SPELING = 0.2     # pen kleiner dan kerndiameter D1 (printmaat)
RIBBEL  = 0.5     # ribbeltop zo ver tussen kern en nominaal (0 = kern, 1 = nominaal)
LENGTE  = 12.0
RIB_POS = 3.0     # ribbelmidden gemeten vanaf de punt
PLAAT   = 5.0
ARM_B   = 7.0

def pen(d, P):
    d1 = d - 1.0825 * P                       # kerndiameter inwendig draad
    rp = (d1 - SPELING) / 2
    rr = (d1 + RIBBEL * (d - d1)) / 2
    h = rr - rp
    zc = LENGTE - RIB_POS
    k = 0.4                                   # halve kruinbreedte ribbel
    prof = [(0,-1),(rp,-1),(rp,zc-k-h),(rr,zc-k),(rr,zc+k),(rp,zc+k+h),(rp,LENGTE-0.4),(rp-0.4,LENGTE),(0,LENGTE)]
    stift = m3.Manifold.revolve(m3.CrossSection([prof]), 64)
    w = min(1.0, rp)                          # gleufbreedte
    gleuf = m3.Manifold.cube((w, 4*rr, 9.0), center=True).translate((0, 0, LENGTE - 4.0 + 0.5))
    stift = stift - gleuf
    me = stift.to_mesh()
    return trimesh.Trimesh(me.vert_properties[:, :3], me.tri_verts), rp, rr

def maak(naam):
    d, P = DRAAD[naam]
    schijf_r = max(9.0, d/2 + 4.0)
    pad = [(0,0),(0,24)]
    pad += [(8+8*np.cos(a), 24+8*np.sin(a)) for a in np.linspace(np.pi, 0, 30)] + [(16,17)]
    profiel = unary_union([LineString(pad).buffer(ARM_B/2, resolution=24),
                           Point(0,0).buffer(schijf_r, resolution=48)])
    plaat = trimesh.creation.extrude_polygon(profiel, PLAAT)
    stift, rp, rr = pen(d, P)
    stift.apply_translation([0, 0, PLAAT])
    mesh = trimesh.boolean.union([plaat, stift], engine="manifold")
    mesh.export(f"kangoo_haakje_pen_{naam}.stl")
    print(naam, "watertight", mesh.is_watertight, "pen ⌀%.2f ribbel ⌀%.2f" % (2*rp, 2*rr), mesh.extents.round(1))
    return profiel, mesh

if __name__ == "__main__":
    fig, ax = plt.subplots(2, 5, figsize=(17,8))
    for i, n in enumerate(DRAAD):
        p, mesh = maak(n)
        x, y = p.exterior.xy
        ax[0,i].fill(x, y, alpha=.4); ax[0,i].set_aspect('equal'); ax[0,i].set_title(n)
        for e in mesh.section(plane_origin=[0,0,0], plane_normal=[0,1,0]).discrete:
            ax[1,i].plot(e[:,0], e[:,2])
        ax[1,i].set_aspect('equal'); ax[1,i].set_title(f"doorsnede {n}")
    plt.tight_layout(); plt.savefig("preview_pen.png", dpi=75)
