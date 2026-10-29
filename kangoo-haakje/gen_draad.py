"""Haakje met aangeprinte schroefdraadstift (M3, M4, M5, M6, M8, ISO-grof) voor de
schroefdraadgaten (vliegtuigboxen) in de Kangoo. Alleen voor lichte belasting (sierverlichting).
Print met de stift OMHOOG: haakje plat op het bed, geen support. Alle maten in mm."""
import numpy as np, trimesh, manifold3d as m3, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Point
from shapely.ops import unary_union

# naam: (nominale diameter, spoed grof)
DRAAD = {"M3": (3.0, 0.5), "M4": (4.0, 0.7), "M5": (5.0, 0.8), "M6": (6.0, 1.0), "M8": (8.0, 1.25)}
SPELING = 0.25     # stift kleiner dan nominaal i.v.m. printmaat; groter = losser
LENGTE  = 12.0     # lengte draadstift
PLAAT   = 5.0      # dikte haakje
ARM_B   = 7.0
T30     = np.tan(np.radians(30))

def draad_stift(d, P, L, rechtsom=True):
    D = 0.6134 * P                      # draaddiepte ISO
    r_maj = (d - SPELING) / 2
    r_min = r_maj - D
    c = 0.125 * P                       # kruinbreedte
    f = T30 * D                         # axiale flankbreedte
    s = [-P/2, -(c/2+f), -c/2, c/2, c/2+f, P/2]
    r = [r_min, r_min, r_maj, r_maj, r_min, r_min]
    th = np.linspace(0, 2*np.pi, 240, endpoint=False)
    sp = (th/(2*np.pi)) * P
    sp = (sp + P/2) % P - P/2
    rad = np.interp(sp, s, r)
    pts = np.c_[rad*np.cos(th), rad*np.sin(th)]
    draai = 360.0 * L / P * (1 if rechtsom else -1)
    cs = m3.CrossSection([pts.tolist()])
    stift = m3.Manifold.extrude(cs, L, n_divisions=int(L/P*48), twist_degrees=draai)
    # afschuining aan de punt
    ch = D + 0.3
    prof = m3.CrossSection([[(0,0),(r_maj+0.05,0),(r_maj+0.05,L-ch),(r_min-0.2,L),(0,L)]])
    kegel = m3.Manifold.revolve(prof, 64)
    stift = stift ^ kegel
    me = stift.to_mesh()
    return trimesh.Trimesh(me.vert_properties[:, :3], me.tri_verts), r_maj, r_min

def maak(naam):
    d, P = DRAAD[naam]
    schijf_r = max(9.0, d/2 + 4.0)
    pad = [(0,0),(0,24)]
    pad += [(8+8*np.cos(a), 24+8*np.sin(a)) for a in np.linspace(np.pi, 0, 30)] + [(16,17)]
    profiel = unary_union([LineString(pad).buffer(ARM_B/2, resolution=24),
                           Point(0,0).buffer(schijf_r, resolution=48)])
    plaat = trimesh.creation.extrude_polygon(profiel, PLAAT)
    stift, r_maj, r_min = draad_stift(d, P, LENGTE)
    stift.apply_translation([0, 0, PLAAT - 1.0])    # 1 mm overlap in de plaat
    mesh = trimesh.boolean.union([plaat, stift], engine="manifold")
    mesh.export(f"kangoo_haakje_draad_{naam}.stl")
    print(naam, "watertight", mesh.is_watertight, "bbox", mesh.extents.round(1))
    return profiel, mesh, stift, r_maj, r_min, P

if __name__ == "__main__":
    fig, ax = plt.subplots(2, 5, figsize=(17,8))
    for i, n in enumerate(DRAAD):
        p, mesh, stift, rmaj, rmin, P = maak(n)
        x, y = p.exterior.xy
        ax[0,i].fill(x, y, alpha=.4); ax[0,i].set_aspect('equal'); ax[0,i].set_title(n)
        for e in mesh.section(plane_origin=[0,0,0], plane_normal=[0,1,0]).discrete:
            ax[1,i].plot(e[:,0], e[:,2]); 
        ax[1,i].set_aspect('equal'); ax[1,i].set_title(f"doorsnede {n} (spoed {P})")
    plt.tight_layout(); plt.savefig("preview_draad.png", dpi=75)
