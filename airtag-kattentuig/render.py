#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Previews + doorsneden van de AirTag-houder. Doorsneden zijn het echte bewijs."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import airtag_houder as A

houder, tag = A.maak_houder(), A.tag_dummy()


# ---------------------------------------------------------------- 3D preview
def vlakken(ax, mesh, kleur, alpha=1.0, licht=(0.4, 0.5, 0.75)):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    L = np.array(licht) / np.linalg.norm(licht)
    sc = 0.35 + 0.65 * np.clip(mesh.face_normals @ L, 0, 1)
    kl = np.array(matplotlib.colors.to_rgb(kleur))
    ax.add_collection3d(Poly3DCollection(
        mesh.vertices[mesh.faces],
        facecolors=np.clip(sc[:, None] * kl, 0, 1), edgecolors="none", alpha=alpha))


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


preview("preview_houder.png", [(houder, "#3f6d99", 1.0)], elev=26, azim=-52,
        titel="Eén stuk — tagholte met lip, riemtunnel eronder")

tag_ex = tag.copy(); tag_ex.apply_translation([0, 0, 14])
preview("preview_inleggen.png",
        [(houder, "#3f6d99", 1.0), (tag_ex, "#c9a227", 1.0)], elev=20, azim=-52,
        titel="De tag klikt van bovenaf onder de lip")

preview("preview_onderkant.png", [(houder, "#2f5878", 1.0)], elev=-30, azim=-52,
        titel="Onderkant — riemtunnel dwars door de voet")


# ---------------------------------------------------------------- doorsneden
def snede(ax, mesh, normaal, kleur, lw=1.4):
    s = mesh.section(plane_origin=[0, 0, A.z_top/2], plane_normal=normaal)
    if s is None:
        return
    for ent in s.entities:
        p = s.vertices[ent.points]
        ax.plot(p[:, 0] if normaal[1] else p[:, 1], p[:, 2], color=kleur, lw=lw)


def maatlijn(ax, x0, x1, z, tekst, kleur="#b03030"):
    ax.annotate("", xy=(x1, z), xytext=(x0, z),
                arrowprops=dict(arrowstyle="<->", color=kleur, lw=1.0))
    ax.text((x0+x1)/2, z+0.4, tekst, color=kleur, ha="center", va="bottom", fontsize=8)


fig, axes = plt.subplots(1, 2, figsize=(15, 6.5))
for ax, n, naam in ((axes[0], [0, 1, 0], "Doorsnede LANGS de riem (XZ)"),
                    (axes[1], [1, 0, 0], "Doorsnede DWARS op de riem (YZ)")):
    snede(ax, houder, n, "#14425e")
    snede(ax, tag, n, "#c9a227")
    ax.set_title(naam, fontsize=11); ax.set_aspect("equal"); ax.grid(alpha=0.25)
    ax.set_xlabel("mm"); ax.set_ylabel("hoogte (mm), 0 = tegen de kat")

ax = axes[0]
maatlijn(ax, -A.SLEUF_B/2, A.SLEUF_B/2, A.z_sleuf0 - 2.4, "riemsleuf 15 mm")
maatlijn(ax, -A.R_LIP, A.R_LIP, A.z_top + 1.6, f"opening Ø{2*A.R_LIP:.1f}")
ax.annotate(f"tag Ø{A.TAG_D:.0f} x {A.TAG_H:.0f}", xy=(0, A.z_vloer + A.TAG_H/2),
            color="#8a6d0b", fontsize=9, ha="center", va="center")
ax.annotate(f"totale hoogte {A.z_top:.1f} mm", xy=(-A.BAR_L/2, A.z_top + 3.0),
            color="#333", fontsize=9)

fig.suptitle("AirTag-houder kattentuig — maatcontrole", fontsize=13)
fig.tight_layout(); fig.savefig("doorsneden.png", dpi=120); plt.close(fig)
print("-> doorsneden.png")


# ------------------------------------------------- detail lip + overhangcontrole
fig, ax = plt.subplots(figsize=(7.5, 7))
snede(ax, houder, [0, 1, 0], "#14425e", lw=2.2)
snede(ax, tag, [0, 1, 0], "#c9a227", lw=1.4)
ax.plot([A.R_HOLTE, A.R_HOLTE - (A.z_top - A.z_lip0)], [A.z_lip0, A.z_top],
        color="#b03030", lw=1.0, ls="--")
ax.text(A.R_HOLTE - 2.6, A.z_top + 0.5, "45° referentie", color="#b03030", fontsize=8)
ax.set_xlim(13.0, 21.5); ax.set_ylim(A.z_vloer - 1.5, A.z_top + 2.0)
ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.set_title(f"Detail lip — {A.LIP} mm overstek onder "
             f"{np.degrees(np.arctan(A.LIP_HELLING)):.0f}° uit het lood\n"
             "de lip blijft binnen de 45°-lijn, dus geen support nodig", fontsize=11)
ax.set_xlabel("radius (mm)"); ax.set_ylabel("hoogte (mm)")
fig.tight_layout(); fig.savefig("detail_lip.png", dpi=130); plt.close(fig)
print("-> detail_lip.png")
