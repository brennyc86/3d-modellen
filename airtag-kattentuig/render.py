#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Previews + doorsneden van de AirTag-houder. Doorsneden zijn het echte bewijs."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly

import airtag_houder as A

kap, voet, tag = A.maak_kap(), A.maak_voet(), A.tag_dummy()


# ---------------------------------------------------------------- 3D preview
def vlakken(ax, mesh, kleur, alpha=1.0, licht=(0.4, 0.5, 0.75)):
    v, f = mesh.vertices, mesh.faces
    tri = v[f]
    n = mesh.face_normals
    L = np.array(licht) / np.linalg.norm(licht)
    sc = 0.35 + 0.65 * np.clip(n @ L, 0, 1)
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    kl = np.array(matplotlib.colors.to_rgb(kleur))
    pc = Poly3DCollection(tri, facecolors=np.clip(sc[:, None] * kl, 0, 1),
                          edgecolors="none", alpha=alpha)
    ax.add_collection3d(pc)


def preview(bestand, delen, elev=24, azim=-58, titel=""):
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    for m, kl, al in delen:
        vlakken(ax, m, kl, al)
    alle = np.vstack([m.vertices for m, _, _ in delen])
    c = alle.mean(axis=0)
    r = (alle.max(axis=0) - alle.min(axis=0)).max() / 2 * 1.05
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off(); ax.set_title(titel, fontsize=12)
    fig.tight_layout(); fig.savefig(bestand, dpi=110); plt.close(fig)
    print("->", bestand)


preview("preview_gemonteerd.png",
        [(kap, "#5b7fa6", 1.0), (voet, "#2f4a63", 1.0)],
        titel="Gemonteerd — kap (licht) op voet met riemtunnel (donker)")

kap_ex = kap.copy(); kap_ex.apply_translation([0, 0, 16])
tag_ex = tag.copy(); tag_ex.apply_translation([0, 0, 7])
preview("preview_exploded.png",
        [(kap_ex, "#5b7fa6", 1.0), (tag_ex, "#c9a227", 1.0), (voet, "#2f4a63", 1.0)],
        elev=18, titel="Opengewerkt — tag (goud) laadt van onderaf in de kap")

preview("preview_onderkant.png",
        [(kap, "#5b7fa6", 1.0), (voet, "#2f4a63", 1.0)],
        elev=-32, azim=-58, titel="Onderkant — riemtunnel 15 x 8 mm dwars door de voet")


# ---------------------------------------------------------------- doorsneden
def snede(ax, mesh, normaal, kleur, lw=1.4):
    s = mesh.section(plane_origin=[0, 0, (A.z0+A.z_top)/2], plane_normal=normaal)
    if s is None:
        return
    p, _ = s.to_2D(to_2D=np.eye(4) if False else None)
    # handmatig projecteren: X of Y tegen Z
    for ent in s.entities:
        pts = s.vertices[ent.points]
        if normaal[1]:      # snede in het XZ-vlak
            ax.plot(pts[:, 0], pts[:, 2], color=kleur, lw=lw)
        else:               # snede in het YZ-vlak
            ax.plot(pts[:, 1], pts[:, 2], color=kleur, lw=lw)


def maatlijn(ax, x0, x1, z, tekst, kleur="#b03030", dz=0.0):
    ax.annotate("", xy=(x1, z), xytext=(x0, z),
                arrowprops=dict(arrowstyle="<->", color=kleur, lw=1.0))
    ax.text((x0+x1)/2, z+dz, tekst, color=kleur, ha="center", va="bottom", fontsize=8)


fig, axes = plt.subplots(1, 2, figsize=(15, 7))

for ax, normaal, naam in ((axes[0], [0, 1, 0], "Doorsnede LANGS de riem (XZ)"),
                          (axes[1], [1, 0, 0], "Doorsnede DWARS op de riem (YZ)")):
    snede(ax, kap, normaal, "#1f5fa0")
    snede(ax, voet, normaal, "#0d3552")
    snede(ax, tag, normaal, "#c9a227")
    ax.axhline(A.z_flens1, color="#999", lw=0.6, ls=":")
    ax.set_title(naam, fontsize=11)
    ax.set_aspect("equal"); ax.grid(alpha=0.25)
    ax.set_xlabel("mm"); ax.set_ylabel("hoogte (mm), 0 = tegen de kat")

# maatvoering op de langsdoorsnede
ax = axes[0]
maatlijn(ax, -A.SLEUF_B/2, A.SLEUF_B/2, A.z_sleuf0 - 1.6, "riemsleuf 15 mm breed")
maatlijn(ax, -A.BAR_L/2, A.BAR_L/2, -3.2, f"tunnel {A.BAR_L:.1f} mm")
ax.annotate(f"sleuf {A.SLEUF_H:.0f} mm hoog", xy=(A.BAR_L/2+1, (A.z_sleuf0+A.z_sleuf1)/2),
            color="#b03030", fontsize=8, va="center")
ax.annotate(f"tag  {A.TAG_D:.0f} x {A.TAG_H:.0f} mm",
            xy=(0, (A.z_plug1+A.z_holte1)/2), color="#8a6d0b", fontsize=9,
            ha="center", va="center")
ax.annotate(f"totale hoogte {A.z_top:.1f} mm", xy=(-A.BAR_L/2, A.z_top+1.5),
            color="#333", fontsize=9)

fig.suptitle("AirTag-houder kattentuig — maatcontrole", fontsize=13)
fig.tight_layout()
fig.savefig("doorsneden.png", dpi=120)
plt.close(fig)
print("-> doorsneden.png")


# --------------------------------------------------- detail van de kliksluiting
fig, ax = plt.subplots(figsize=(7, 7))
snede(ax, kap, [0, 1, 0], "#1f5fa0", lw=2.0)
snede(ax, voet, [0, 1, 0], "#0d3552", lw=2.0)
snede(ax, tag, [0, 1, 0], "#c9a227", lw=1.2)
ax.set_xlim(14.5, 21.5); ax.set_ylim(A.z_flens1 - 3.0, A.z_plug1 + 2.0)
ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_title(f"Detail kliksluiting (overlap {A.KLIK} mm)\n"
             f"blauw = kap, donker = voet, goud = tag", fontsize=11)
ax.set_xlabel("radius (mm)"); ax.set_ylabel("hoogte (mm)")
fig.tight_layout(); fig.savefig("detail_klik.png", dpi=130); plt.close(fig)
print("-> detail_klik.png")
